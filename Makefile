# Docker komutları için kolaylaştırıcı Makefile

.PHONY: build up down logs shell migrate seed test clean

# Docker Compose komutları
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

# Geliştirme komutları
shell:
	docker-compose exec web python manage.py shell

migrate:
	docker-compose exec web python manage.py migrate

seed:
	docker-compose exec web python manage.py seed_data

test:
	docker-compose exec web python manage.py test

# Veritabanı sıfırlama
reset-db:
	docker-compose down
	docker volume rm drf_case_postgres_data
	docker-compose up -d
	docker-compose exec web python manage.py migrate
	docker-compose exec web python manage.py seed_data

# Temizlik
clean:
	docker-compose down --volumes --remove-orphans
	docker system prune -f

# Production
prod-build:
	docker-compose -f docker-compose.prod.yml build

prod-up:
	docker-compose -f docker-compose.prod.yml up -d

prod-down:
	docker-compose -f docker-compose.prod.yml down

# Yardım
help:
	@echo "Kullanılabilir komutlar:"
	@echo "  build      - Docker image'larını oluştur"
	@echo "  up         - Servisleri başlat"
	@echo "  down       - Servisleri durdur"
	@echo "  logs       - Log'ları görüntüle"
	@echo "  shell      - Django shell'e bağlan"
	@echo "  migrate    - Veritabanı migration'larını çalıştır"
	@echo "  seed       - Test verilerini yükle"
	@echo "  test       - Testleri çalıştır"
	@echo "  reset-db   - Veritabanını sıfırla ve test verilerini yükle"
	@echo "  clean      - Docker temizliği yap"
	@echo "  prod-*     - Production komutları"
