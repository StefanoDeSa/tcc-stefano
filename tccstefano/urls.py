from django.contrib import admin
from django.urls import path, include
from oauth2_provider import urls as oauth2_urls
from tccstefano.api.viewsets import CustomUserList


urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include(oauth2_urls)),
    path('api/users/', CustomUserList.as_view(), name='api_users'),
    path('', include('sso_auth.urls')),
]
