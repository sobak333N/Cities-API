FROM python:3.11-slim

WORKDIR /app

COPY ./app/requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt 

COPY . .

CMD ["gunicorn", "app.main:init_app()", "-w", "4", "-k", "aiohttp.GunicornWebWorker", "--bind", "0.0.0.0:8000"]
# CMD ["sh", "-c", "python3 -m app.main"]

