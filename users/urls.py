from django.urls import path

from users.views import UserViewSet, LoginView, LogoutView, CurrentUserView, approveUser
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register("users", UserViewSet)


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("me/", CurrentUserView.as_view(), name="me"),
    path("verify-user/", approveUser),
] + router.urls
