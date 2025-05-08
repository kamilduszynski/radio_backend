FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y postgresql-client

COPY . .

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
