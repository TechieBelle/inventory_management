from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserViewSet, RegisterView

router = DefaultRouter()
router.register("users", UserViewSet)

urlpatterns = [
    # JWT Auth
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Registration
    path("register/", RegisterView.as_view(), name="register"),

    # User CRUD via ViewSet
    path("", include(router.urls)),
]
