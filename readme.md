```bash
# Start services (with build)
prod.bat up

# Stop services (including volumes)
prod.bat down

# Restart services
prod.bat restart

# Check service status
prod.bat status

# Show logs
prod.bat logs

# Clear cache
prod.bat cleancache

# Run tests
prod.bat test

# Health check
prod.bat health

# Seed data
prod.bat data
```

## API Endpoints

- **Users:** `/api/users/`
- **Flights:** `/api/flights/`
- **Crew:** `/api/crew/`

## Technologies

- Django REST Framework
- PostgreSQL
- Redis (Celery)
- Docker
- Nginx
- Gunicorn
- JWT