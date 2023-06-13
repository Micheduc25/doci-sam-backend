from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from .permissions import IsCurrentUser
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)

from users.serializers import LoginSerializer, UserSerializer
from users.models import CustomUser


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsAuthenticated]
        elif self.action == "create":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsCurrentUser | permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({"user": serializer.data})


class LoginView(APIView):
    def authenticate(self, username, password):
        try:
            matching_user = CustomUser.objects.get(username=username)

            if matching_user.password != password:
                return None

            return matching_user
        except CustomUser.DoesNotExist:
            return None

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            username = serializer.data["username"]
            password = serializer.data["password"]

            user = self.authenticate(username=username, password=password)

            if user is not None:
                try:
                    token = Token.objects.get(user_id=user.id)
                except Token.DoesNotExist:
                    token = Token.objects.create(user=user)
                    token.save()

                user_serializer = UserSerializer(user)
                return Response({"user": user_serializer.data, "token": token.key})

            else:
                return Response({"error": "Invalid username or password"}, status=404)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = Token.objects.get(user_id=request.user.id)

            token.delete()
            return Response("Success")

        except Token.DoesNotExist:
            return Response({"error": "User is not authenticarted"}, status=404)
