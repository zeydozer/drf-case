```bash
# Servisleri başlat (build ile birlikte)
prod.bat up

# Servisleri durdur (volumes ile birlikte)
prod.bat down

# Servisleri yeniden başlat
prod.bat restart

# Servis durumunu kontrol et
prod.bat status

# Logları görüntüle
prod.bat logs

# Cache temizle
prod.bat cleancache

# Testleri çalıştır
prod.bat test

# Health check
prod.bat health
```

## API Endpoints

- **Users:** `/api/users/`
- **Flights:** `/api/flights/`  
- **Crew:** `/api/crew/`

## Teknolojiler

- Django REST Framework
- PostgreSQL
- Redis (Celery)
- Docker
- Nginx
- Gunicorn
- JWT