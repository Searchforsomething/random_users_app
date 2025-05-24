import random

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'


class RandomUserView(APIView):
    def get(self, request):
        count = User.objects.count()
        if count == 0:
            return Response({'detail': 'No users in database.'})
        random_user = User.objects.all()[random.randint(0, count - 1)]
        return Response(UserSerializer(random_user).data)
