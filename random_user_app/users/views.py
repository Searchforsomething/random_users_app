import json
import random

from django.views.decorators.csrf import csrf_exempt
from django.core.management import call_command
from django.http import JsonResponse
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


@csrf_exempt
def trigger_load_users(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            count = int(data.get("count", 100))
            call_command("load_random_users", count=count)
            return JsonResponse({"status": "ok", "message": f"{count} users loaded."})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"error": "Only POST allowed"}, status=405)