# DRF Case - Uçuş Yönetim Sistemi

Django REST Framework kullanılarak geliştirilmiş basit bir uçuş yönetim sistemi.

## Özellikler

- **Uçuş Yönetimi**: Uçuş bilgilerini görüntüleme, oluşturma ve güncelleme
- **Mürettebat Yönetimi**: Pilot, co-pilot ve kabin görevlilerinin uçuşlara atanması
- **Bildirim Sistemi**: Celery ile asenkron uçuş gecikme bildirimleri
- **REST API**: Django REST Framework ile tam API desteği
- **Docker Desteği**: Geliştirme ve production ortamları için Docker konfigürasyonu

## Teknolojiler

- Django 5.2.4
- Django REST Framework
- Celery (Asenkron görevler)
- PostgreSQL (Production) / SQLite (Development)
- Redis (Celery broker)
- Docker & Docker Compose

## Docker ile Kurulum (Önerilen)

1. **Projeyi klonlayın:**
   ```bash
   git clone <repository-url>
   cd drf_case
   ```

2. **Docker ile çalıştırın:**
   ```bash
   # Servisleri başlat
   docker-compose up -d
   
   # Migration'ları çalıştır
   docker-compose exec web python manage.py migrate
   
   # Test verilerini yükle
   docker-compose exec web python manage.py seed_data
   ```

3. **Uygulamayı test edin:**
   - API: http://localhost:8000/api/
   - Admin: http://localhost:8000/admin/

## Makefile Komutları

```bash
make build      # Docker image'larını oluştur
make up         # Servisleri başlat
make down       # Servisleri durdur
make logs       # Log'ları görüntüle
make shell      # Django shell'e bağlan
make migrate    # Migration'ları çalıştır
make seed       # Test verilerini yükle
make reset-db   # Veritabanını sıfırla
make clean      # Docker temizliği
```

## Manuel Kurulum

1. **Bağımlılıkları yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Veritabanını hazırlayın:**
   ```bash
   python manage.py migrate
   ```

3. **Süper kullanıcı oluşturun:**
   ```bash
   python manage.py createsuperuser
   ```

4. **Sunucuyu başlatın:**
   ```bash
   python manage.py runserver
   ```

5. **Celery worker'ı başlatın (ayrı terminal):**
   ```bash
   celery -A drf_case worker --loglevel=info
   ```

## API Endpoints

- `/flights/` - Uçuş listesi ve oluşturma
- `/crew/` - Mürettebat listesi ve oluşturma
- `/admin/` - Django admin paneli

## Proje Yapısı

- `flights/` - Uçuş modeli ve API'leri
- `crew/` - Mürettebat modeli ve API'leri  
- `notifications/` - Celery görevleri
- `drf_case/` - Ana proje ayarları

## Kullanım

1. Admin panelinden uçuş bilgilerini ekleyin
2. Mürettebat üyelerini uçuşlara atayın
3. API endpoints üzerinden veri okuma/yazma işlemleri yapın
4. Uçuş durumu "delayed" olarak güncellendiğinde otomatik bildirim gönderilir