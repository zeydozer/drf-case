# DRF Case - Uçuş Yönetim Sistemi

Django REST Framework kullanılarak geliştirilmiş basit bir uçuş yönetim sistemi.

## Özellikler

- **Uçuş Yönetimi**: Uçuş bilgilerini görüntüleme, oluşturma ve güncelleme
- **Mürettebat Yönetimi**: Pilot, co-pilot ve kabin görevlilerinin uçuşlara atanması
- **Bildirim Sistemi**: Celery ile asenkron uçuş gecikme bildirimleri
- **REST API**: Django REST Framework ile tam API desteği

## Teknolojiler

- Django 5.2.4
- Django REST Framework
- Celery (Asenkron görevler)
- SQLite (Veritabanı)

## Kurulum

1. **Bağımlılıkları yükleyin:**
   ```bash
   pip install django djangorestframework celery
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