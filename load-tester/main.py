from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import httpx, asyncio, random, time
from httpx import Limits, Timeout
import pathlib

TARGET_URL = "http://51.250.88.180/city/get/"
PAGE_SIZE  = 20          
MAX_PAGE   = 10          

app = FastAPI(title="Load-Tester (GET)")

@app.get("/")
async def root():
    return {"msg": "GET load-tester ready"}

async def fire_gets(client, rps: int, duration: int) -> tuple[int, int]:
    succ = fail = 0
    stop     = time.monotonic() + duration
    interval = 1 / rps
    sem      = asyncio.Semaphore(rps)   

async def fire_gets(client, rps: int, duration: int) -> tuple[int, int]:
    succ = fail = 0
    interval = 1 / rps
    total    = rps * duration
    sem      = asyncio.Semaphore(rps)
    tasks: list[asyncio.Task] = []

    async def one_get():
        nonlocal succ, fail
        page = random.randint(1, MAX_PAGE)          
        url  = f"{TARGET_URL}?page={page}"
        async with sem:
            try:
                resp = await client.get(url, headers={"accept": "application/json"})
                print("→", resp.status_code, url)
                if resp.status_code < 400:
                    succ += 1          
                else:
                    fail += 1
            except Exception as exc:
                print("EXC", type(exc).__name__, url)
                fail += 1


    for _ in range(total):
        tasks.append(asyncio.create_task(one_get()))
        await asyncio.sleep(interval)

    await asyncio.gather(*tasks, return_exceptions=True)
    return succ, fail


@app.post("/start")
async def start(
    rps: int = Form(...),
    duration: int = Form(1),          
):
    limits  = Limits(max_connections=rps, max_keepalive_connections=rps)
    timeout = Timeout(5.0)           

    async with httpx.AsyncClient(timeout=timeout, limits=limits) as client:
        succ, fail = await fire_gets(client, rps, duration)

    return {
        "endpoint": TARGET_URL,
        "pages": f"1‒{MAX_PAGE}",
        "seconds": duration,
        "rps": rps,
        "success": succ,
        "fail": fail,
    }

HTML = """
<!DOCTYPE html><html lang="ru"><meta charset="utf-8">
<title>Load-Tester GET</title>
<style>
 body{font-family:sans-serif;max-width:420px;margin:2rem auto}
 input,button{padding:.4rem .6rem;margin:.3rem 0;width:100%}
 button{cursor:pointer}pre{background:#f4f4f4;padding:.6rem}
</style>
<h2>Load-Tester (GET /city/get)</h2>
<form id="frm">
  <label>RPS:<input name="rps" type="number" min="1" value="5" required></label>
  <label>Duration (sec):<input name="duration" type="number" min="1" value="1"></label>
  <button type="submit">Start</button>
</form>
<h3>Server reply</h3><pre id="out">–</pre>
<script>
document.getElementById('frm').addEventListener('submit',async e=>{
  e.preventDefault();
  const fd=new FormData(e.target);
  const r=await fetch('/start',{method:'POST',body:fd});
  document.getElementById('out').textContent=await r.text();
});
</script>
"""

@app.get("/ui", response_class=HTMLResponse)
async def ui():  
    return HTML
