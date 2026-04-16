from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # ВОТ ЭТОЙ СТРОЧКИ НЕ ХВАТАЕТ!

app_name = 'account'

urlpatterns = [
    # Стандартные вьюхи Django для входа/выхода
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Твоя вьюха для регистрации
    path('register/', views.register, name='register'),
]