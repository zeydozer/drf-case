# Bu, Django'nun başlatıldığında Celery uygulamasının yüklenmesini sağlar
from .celery import app as celery_app

__all__ = ('celery_app',)