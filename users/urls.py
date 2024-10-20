from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserUpdateAPIView, UserRetrieveAPIView

app_name = UsersConfig.name
router = SimpleRouter()

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('register/', UserCreateAPIView.as_view(), name='user_register'),
    path('<int:pk>/update/', UserUpdateAPIView.as_view(), name='user_update'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='user_get'),
]


urlpatterns += router.urls