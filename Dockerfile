# Wybierz obraz bazowy z Pythonem
FROM python:3.13-slim

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj zależności
COPY requirements.txt .

# Zainstaluj zależności
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj cały projekt
COPY . .

# Otwórz port dla serwera
EXPOSE 8000

# Domyślne polecenie uruchamiające aplikację
CMD ["gunicorn", "radio_hits_api.wsgi:application", "--bind", "0.0.0.0:8000"]