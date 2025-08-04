#!/bin/bash

# Entrypoint script for Docker container

set -e

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting Django application...${NC}"

# Veritabanının hazır olmasını bekle
echo -e "${YELLOW}⏳ Waiting for database...${NC}"
python manage.py wait_for_db 2>/dev/null || echo "Database ready"

# Migration'ları çalıştır
echo -e "${YELLOW}📦 Running migrations...${NC}"
python manage.py migrate --noinput

# Static dosyaları topla
echo -e "${YELLOW}📁 Collecting static files...${NC}"
python manage.py collectstatic --noinput

# Superuser oluştur (eğer yoksa)
echo -e "${YELLOW}👤 Creating superuser...${NC}"
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
EOF

echo -e "${GREEN}✅ Setup completed!${NC}"

# Django'yu başlat
exec "$@"
