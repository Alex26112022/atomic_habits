from django.urls import path

from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('', UserListAPIView.as_view(), name='user_list'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user_detail'),
    path('create/', UserCreateAPIView.as_view(), name='user_create'),
    path('<int:pk>/update/', UserUpdateAPIView.as_view(),
         name='user_update'),
    path('<int:pk>/delete/', UserDestroyAPIView.as_view(),
         name='user_delete'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
         name='login'),
    path('refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)),
         name='refresh'),
]
