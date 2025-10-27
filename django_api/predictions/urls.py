# Este es el archivo: django_api/titanic_api/urls.py

from django.contrib import admin
from django.urls import path, include  # <-- ¡Asegúrate de importar 'include'!

urlpatterns = [
    path('admin/', admin.site.urls),

    # AÑADE ESTA LÍNEA:
    # Esto le dice a Django que cualquier URL que empiece con 'api/'
    # debe ser manejada por el archivo 'urls.py' de tu app 'predictions'.
    path('api/', include('predictions.urls')), 
]
