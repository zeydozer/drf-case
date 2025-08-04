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

prod-logs:
	docker-compose -f docker-compose.prod.yml logs -f

prod-migrate:
	docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

prod-collectstatic:
	docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

prod-shell:
	docker-compose -f docker-compose.prod.yml exec web python manage.py shell

prod-deploy: prod-build prod-up prod-migrate prod-collectstatic
	@echo "Production deployment completed!"

prod-restart:
	docker-compose -f docker-compose.prod.yml restart web nginx

# SSL sertifikası için (Let's Encrypt)
ssl-setup:
	@echo "SSL setup için aşağıdaki komutları çalıştırın:"
	@echo "1. certbot kurulumu:"
	@echo "   docker run -it --rm --name certbot -v \"/etc/letsencrypt:/etc/letsencrypt\" -v \"/var/lib/letsencrypt:/var/lib/letsencrypt\" -p 80:80 certbot/certbot certonly --standalone"
	@echo "2. nginx.conf dosyasını SSL için güncelleyin"
	@echo "3. prod-restart komutunu çalıştırın"

# Yardım
help:
	@echo "Kullanılabilir komutlar:"
	@echo "  build         - Docker image'larını oluştur"
	@echo "  up            - Servisleri başlat"
	@echo "  down          - Servisleri durdur"
	@echo "  logs          - Log'ları görüntüle"
	@echo "  shell         - Django shell'e bağlan"
	@echo "  migrate       - Veritabanı migration'larını çalıştır"
	@echo "  seed          - Test verilerini yükle"
	@echo "  test          - Testleri çalıştır"
	@echo "  reset-db      - Veritabanını sıfırla ve test verilerini yükle"
	@echo "  clean         - Docker temizliği yap"
	@echo ""
	@echo "Production komutları:"
	@echo "  prod-build    - Production image'larını oluştur"
	@echo "  prod-up       - Production servisleri başlat"
	@echo "  prod-down     - Production servisleri durdur"
	@echo "  prod-logs     - Production log'ları görüntüle"
	@echo "  prod-migrate  - Production migration'ları çalıştır"
	@echo "  prod-deploy   - Tam production deployment"
	@echo "  prod-restart  - Web ve nginx servislerini yeniden başlat"
	@echo "  ssl-setup     - SSL sertifikası kurulum rehberi"
