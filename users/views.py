from rest_framework import generics
from rest_framework.permissions import AllowAny
from users.serializer import UserProfileSerializer
from users.models import UserProfile


# Create your views here.
class UserProfileCreateAPIView(generics.CreateAPIView):
    query_set = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (AllowAny,)
