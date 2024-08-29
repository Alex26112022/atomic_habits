from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, CreateAPIView, \
    RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser

from users.permissions import IsUser
from users.serializers import UserSerializer


class UserListAPIView(ListAPIView):
    user = get_user_model()
    queryset = user.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserCreateAPIView(CreateAPIView):
    user = get_user_model()
    queryset = user.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveAPIView(RetrieveAPIView):
    user = get_user_model()
    queryset = user.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUser | IsAdminUser]


class UserUpdateAPIView(UpdateAPIView):
    user = get_user_model()
    queryset = user.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUser]

    def perform_update(self, serializer):
        user = serializer.save(is_active=True)
        if self.request.data.get('password') is not None:
            user.set_password(user.password)
        user.save()


class UserDestroyAPIView(DestroyAPIView):
    user = get_user_model()
    queryset = user.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUser | IsAdminUser]
