from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUser, CustomUserSerializer

class CustomUserList(generics.ListAPIView):
    permission_classes = []
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)