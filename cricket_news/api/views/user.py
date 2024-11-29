from rest_framework import generics, permissions
from django.contrib.auth.models import User
from ..serializers.user import UserSerializer

class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user