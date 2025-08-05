from django.contrib import admin
from django.urls import path
from django.urls import include
from django.http import JsonResponse
from django.views.decorators.cache import never_cache

@never_cache
def health_check(request):
  """Simple health check endpoint for load balancer/monitoring"""
  return JsonResponse({"status": "healthy", "service": "drf_case"})

@never_cache
def home_view(request):
  """Home page with API information"""
  return JsonResponse({
    "message": "Welcome to DRF Case - Flight Operations API",
    "version": "1.0.0",
    "endpoints": {
      "admin": "/admin/",
      "api_flights": "/api/flights/",
      "api_crew": "/api/crew/",
      "health": "/health/"
    },
    "domain": "drf.kuzeyyedekparca.com",
    "status": "running"
  })

urlpatterns = [
  path('', home_view, name='home'),
  path('admin/', admin.site.urls),
  path('api/', include('flights.urls')),
  path('api/', include('crew.urls')),
  path('health/', health_check, name='health_check'),
  path('api/users/', include('users.urls')),
]

# Importing JWT views for token management
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns += [
  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
