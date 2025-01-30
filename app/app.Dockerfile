FROM python:3.11-slim

WORKDIR /app

COPY ./app/requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt 

COPY . .

# CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000"]
CMD ["sh", "-c", "python3 -m app.main"]

