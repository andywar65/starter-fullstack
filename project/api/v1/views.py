from rest_framework import generics

from users.models import User
from .serializers import *

class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
