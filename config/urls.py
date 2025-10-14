from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), # Usamos la vista 'home' directamente
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)