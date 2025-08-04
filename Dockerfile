# Python 3.12 tabanlı resmi image kullan (3.13 ile psycopg2 uyumlu değil)
FROM python:3.12-slim

# Sistem güncellemeleri ve gerekli paketler
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Çalışma dizinini ayarla
WORKDIR /app

# Python buffering'i kapat (log'lar için)
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Requirements dosyasını kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# Static dosyalar dizinini oluştur
RUN mkdir -p /app/staticfiles

# Migration'ları çalıştır ve static dosyaları topla
RUN python manage.py collectstatic --noinput

# Port 8000'i aç
EXPOSE 8000

# Health check ekle
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/api/flights/', timeout=10)" || exit 1

# Django development server'ı başlat
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
