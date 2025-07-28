FROM python:3.11-slim

ENV PROMETHEUS_MULTIPROC_DIR=/tmp/prometheus_multiproc
RUN mkdir -p /tmp/prometheus_multiproc
VOLUME /tmp/prometheus_multiproc

WORKDIR /app

COPY ./app/requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "app.main:init_app()", "-w", "4", "-k", "aiohttp.GunicornWebWorker", "--bind", "0.0.0.0:8000"]
