from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import generics, permissions
from .serializers import CustomUser, CustomUserSerializer

class CustomUserList(generics.ListAPIView):
    permission_classes = []
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer