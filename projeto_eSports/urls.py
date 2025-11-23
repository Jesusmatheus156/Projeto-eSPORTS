# projeto_eSports/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # <-- IMPORTAR
from django.conf.urls.static import static # <-- IMPORTAR

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_eSports.urls')),

    # Adicione esta linha para o uploader:
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

# Adicione esta linha no final:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)