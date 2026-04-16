from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'shop'

# Роутер для API (Проект 4)
router = DefaultRouter()
router.register(r'products-api', views.ProductViewSet, basename='product-api')

urlpatterns = [
    # 1. Главная
    path('', views.product_list, name='product_list'),
    path('contact/', views.contact_view, name='contact'),
    
    # 2. КОРЗИНА (Должна быть выше категорий!)
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    
    # 3. Избранное (Тоже выше категорий)
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('favorite/add/<int:product_id>/', views.add_to_favorite, name='add_to_favorite'),
    
    # 4. API (Проект 4)
    path('api/', include(router.urls)),

    # 5. Детальная страница товара (Проект 1)
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),

    # 6. КАТЕГОРИИ (САМЫЙ НИЗ)
    # Этот путь должен быть последним, иначе он "съест" /cart/ и /favorites/
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),

    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
]