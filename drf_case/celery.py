import os
from celery import Celery

# Django ayarlarını varsayılan olarak ayarla
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_case.settings')

app = Celery('drf_case')

# Django settings'ten celery konfigürasyonunu oku
app.config_from_object('django.conf:settings', namespace='CELERY')

# Django uygulamalarından task'ları otomatik olarak keşfet
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
