from aiohttp import web
from prometheus_client import (
    Counter, Histogram, Gauge,
    generate_latest, CONTENT_TYPE_LATEST,
    CollectorRegistry, multiprocess
)

REQ_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "handler", "status"],
)

LATENCY = Histogram(
    "http_request_duration_seconds",
    "Request latency (seconds)",
    ["handler"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 3, 5, 10),
)

INFLIGHT = Gauge(
    "http_in_flight_requests",
    "In-flight requests",
)

@web.middleware
async def prom_middleware(request: web.Request, handler):
    route = (
        request.match_info.route.resource.canonical
        if request.match_info.route else "unknown"
    )
    INFLIGHT.inc()
    try:
        with LATENCY.labels(handler=route).time():
            resp = await handler(request)
    finally:
        INFLIGHT.dec()

    REQ_TOTAL.labels(
        method=request.method,
        handler=route,
        status=resp.status,
    ).inc()
    return resp

async def metrics_endpoint(request):
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    data = generate_latest(registry)
    return web.Response(
        body=data,
        headers={"Content-Type": CONTENT_TYPE_LATEST},
    )

def setup_metrics(app: web.Application) -> None:
    app.middlewares.append(prom_middleware)
    app.router.add_get("/metrics", metrics_endpoint)