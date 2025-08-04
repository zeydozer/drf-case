# DRF Case - Uçuş Yönetim Sistemi

Django REST Framework kullanılarak geliştirilmiş basit bir uçuş yönetim sistemi.

## Özellikler

- **Uçuş Yönetimi**: Uçuş bilgilerini görüntüleme, oluşturma ve güncelleme
- **Gelişmiş Filtreleme**: Origin, destination, status ve tarih bazlı filtreleme
- **Sayfalama**: Performanslı sayfa bazlı veri görüntüleme
- **Arama**: Uçuş numarası, origin ve destination alanlarında arama
- **Akıllı Cache**: Redis tabanlı performans optimizasyonu
- **Mürettebat Yönetimi**: Pilot, co-pilot ve kabin görevlilerinin uçuşlara atanması
- **Bildirim Sistemi**: Celery ile asenkron uçuş gecikme bildirimleri
- **REST API**: Django REST Framework ile tam API desteği
- **Docker Desteği**: Geliştirme ve production ortamları için Docker konfigürasyonu

## Teknolojiler

- Django 5.2.4
- Django REST Framework
- Django Filters (Filtreleme desteği)
- Celery (Asenkron görevler)
- PostgreSQL (Production) / SQLite (Development)
- Redis (Celery broker ve Cache)
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

### Uçuş API'leri
- `GET /api/flights/` - Uçuş listesi (filtreleme ve sayfalama desteği)
- `POST /api/flights/` - Yeni uçuş oluşturma
- `GET /api/flights/{id}/` - Belirli uçuş detayı
- `PUT/PATCH /api/flights/{id}/` - Uçuş güncelleme
- `DELETE /api/flights/{id}/` - Uçuş silme

### Filtreleme Parametreleri
```bash
# Origin filtreleme
GET /api/flights/?origin=Antalya
GET /api/flights/?origin=anta        # Kısmi arama

# Destination filtreleme  
GET /api/flights/?destination=London

# Status filtreleme
GET /api/flights/?status=departed
GET /api/flights/?status=planned,delayed    # Çoklu seçim

# Tarih filtreleme
GET /api/flights/?scheduled_date=2025-08-04
GET /api/flights/?scheduled_time_after=2025-08-04T10:00:00Z
GET /api/flights/?scheduled_time_before=2025-08-05T10:00:00Z

# Arama (flight_number, origin, destination)
GET /api/flights/?search=TK123

# Sıralama
GET /api/flights/?ordering=scheduled_time      # Artan
GET /api/flights/?ordering=-scheduled_time     # Azalan

# Sayfalama
GET /api/flights/?page=1&page_size=10

# Kombinasyon örneği
GET /api/flights/?origin=Antalya&status=departed&page=1&ordering=-scheduled_time
```

### Diğer API'ler
- `/api/crew/` - Mürettebat listesi ve oluşturma
- `/admin/` - Django admin paneli

## Proje Yapısı

- `flights/` - Uçuş modeli, API'leri ve filtreleme sistemi
- `flights/filters.py` - Django Filters ile filtreleme tanımları
- `flights/views.py` - ViewSet'ler, sayfalama ve cache yönetimi
- `crew/` - Mürettebat modeli ve API'leri  
- `notifications/` - Celery görevleri
- `drf_case/` - Ana proje ayarları

## Performans Özellikleri

- **Redis Cache**: Filtresiz istekler için 5 dakika cache
- **Akıllı Cache**: Filtreleme/sayfalama varsa cache devre dışı
- **Sayfalama**: Varsayılan 10 kayıt/sayfa, maksimum 100 kayıt/sayfa
- **Database Optimizasyonu**: Efficient query'ler ve indexleme

## Kullanım

1. Admin panelinden uçuş bilgilerini ekleyin veya test verilerini yükleyin
2. Mürettebat üyelerini uçuşlara atayın
3. API endpoints üzerinden veri okuma/yazma işlemleri yapın
4. Filtreleme, arama ve sayfalama özelliklerini kullanın
5. Uçuş durumu "delayed" olarak güncellendiğinde otomatik bildirim gönderilir

### API Kullanım Örnekleri

```bash
# Antalya'dan kalkan uçuşları listele
curl "http://localhost:8000/api/flights/?origin=Antalya"

# Delayed durumdaki uçuşları bul  
curl "http://localhost:8000/api/flights/?status=delayed"

# TK ile başlayan uçuşları ara
curl "http://localhost:8000/api/flights/?search=TK"

# İlk sayfada 5 kayıt göster
curl "http://localhost:8000/api/flights/?page=1&page_size=5"

# Tarihe göre sıralı uçuşlar
curl "http://localhost:8000/api/flights/?ordering=-scheduled_time"
```