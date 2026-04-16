from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ЭТА СТРОКА ОЖИВИТ ПЕРЕКЛЮЧАТЕЛЬ ЯЗЫКОВ
    path('i18n/', include('django.conf.urls.i18n')),
    
    # Добавляем маршруты для авторизации
    path('account/', include('account.urls', namespace='account')), 
    
    # Главная страница магазина
    path('', include('shop.urls', namespace='shop')),
]

# Для отображения картинок товаров в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)