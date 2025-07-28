FROM python:3.11-slim

ENV PROMETHEUS_MULTIPROC_DIR=/tmp/prometheus_multiproc
RUN mkdir -p $PROMETHEUS_MULTIPROC_DIR \
    && chmod 777 $PROMETHEUS_MULTIPROC_DIR
VOLUME ["/tmp/prometheus_multiproc"]

WORKDIR /app

COPY app/requirements.txt ./
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

COPY app/ ./

CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "aiohttp.GunicornWebWorker", "--bind", "0.0.0.0:8000"]


