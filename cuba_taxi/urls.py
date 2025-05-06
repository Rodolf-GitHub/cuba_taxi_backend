from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .endpoints import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]

# Esta es la parte que está causando el problema
# Configúrala correctamente para que solo sirva archivos de MEDIA_URL
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # NO añadas líneas adicionales que capturen todas las URLs