from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),  # Agora a home está na raiz "/"
    path("accounts/login/", views.CustomLoginView.as_view(), name="login"),  # Usando a nova LoginView personalizada
    path('accounts/', include('django.contrib.auth.urls')),  # URLs padrão do Django
    path('accounts/', include('django.contrib.auth.urls')),  # URLs padrão do Django
    path('register/', views.register, name='register'),  # Cadastro
]
