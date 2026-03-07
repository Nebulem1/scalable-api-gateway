FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir fastapi uvicorn

CMD ["uvicorn", "product_service:app", "--host", "0.0.0.0", "--port", "8001"]