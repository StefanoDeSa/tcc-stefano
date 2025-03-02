from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path("login",views.login_page,name='login'),
    path("logout",views.logout_page,name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path("signup",views.signup_view,name='signup'),
    path('verify_2fa/', views.verify_2fa, name='verify_2fa'),
    path('disable-2fa/', views.disable_2fa, name='disable_2fa'),
]
