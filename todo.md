## 🧠 Case: **FlightOps – Uçuş Operasyon Yönetim Sistemi (DRF)**

### 🎯 Hedef

Django REST Framework ile mikroservis mimarisine yakın modüler bir yapı kurarak uçuş, ekip ve bildirim süreçlerini yöneten bir backend uygulaması geliştirmek.

---

## 🧩 Modüller

### 1. **Flight App**

* Uçuş CRUD (Create, Read, Update, Delete)
* Fields: `flight_number`, `origin`, `destination`, `scheduled_time`, `status`
* `status` alanı (planned, delayed, departed, landed)

### 2. **Crew App**

* Ekip CRUD
* Fields: `name`, `role`, `assigned_flight` (FK)

### 3. **Notification App**

* Signals + Celery ile asenkron bildirim sistemi
* Örn: Uçuş statüsü “delayed” olursa ekibe e-posta/sms/log bildirimi

---

## 🧱 Teknolojiler

| Katman          | Teknoloji                  |
| --------------- | -------------------------- |
| Backend         | Django + DRF               |
| Veritabanı      | PostgreSQL                 |
| Mesaj Kuyruğu   | Redis + Celery             |
| Caching         | Redis                      |
| Queue Tetikleme | Django signals             |
| Deployment      | Docker + Docker Compose    |
| Web Server      | Gunicorn + Nginx           |

## ✅ Yapılacaklar Listesi

### 1. Kurulum ve Konfigürasyon

* [x] Django + DRF kurulumu
* [ ] PostgreSQL bağlantısı
* [ ] Redis bağlantısı

### 2. Flight Uygulaması

* [x] Model, Serializer, ViewSet, URL
* [x] Status değişikliği ile signal tetikleme

### 3. Crew Uygulaması

* [x] Model, Serializer, ViewSet, URL

### 4. Notification Uygulaması

* [x] Signal dinleyici + Celery task
* [ ] “delayed” flight olduğunda mesaj/log üret

### 5. Docker ve Deploy

* [ ] Dockerfile & docker-compose.yml
* [ ] Gunicorn & Nginx konfigürasyonu