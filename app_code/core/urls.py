from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),    
    path('importacao/', views.importacao, name='importacao'),
    path('imprimir_pulseiras/', views.imprimir_pulseiras, name='imprimir_pulseiras'),
       
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)