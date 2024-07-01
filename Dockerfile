FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y curl && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

COPY wait-for-vault.sh /app/wait-for-vault.sh
RUN chmod +x /app/wait-for-vault.sh

COPY scripts/generate_and_store_key.py /app/scripts/generate_and_store_key.py

# Copia el archivo .env al contenedor
COPY .env /app/.env

# Exporta las variables de entorno
RUN echo "export $(cat /app/.env | xargs)" >> /etc/profile

# Establece el PYTHONPATH
ENV PYTHONPATH /app

CMD ["sh", "-c", "/app/wait-for-vault.sh && python /app/scripts/generate_and_store_key.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
