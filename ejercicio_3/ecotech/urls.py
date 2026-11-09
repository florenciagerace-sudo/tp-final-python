from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Todas las direcciones de la app "sustentabilidad"
    path('', include('sustentabilidad.urls')),
]