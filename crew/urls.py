from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CrewMemberViewSet

router = DefaultRouter()
router.register(r'crew', CrewMemberViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
