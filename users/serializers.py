from rest_framework.serializers import Serializer, ModelSerializer, CharField
from users.models import CustomUser


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = [
            "groups",
            "user_permissions",
            "is_active",
            "is_staff",
            "is_superuser",
        ]

    def to_representation(self, instance):
        user_repr = super().to_representation(instance)
        user_repr.pop("password")

        return user_repr


class LoginSerializer(Serializer):
    username = CharField(max_length=15)
    password = CharField(max_length=255, min_length=6)
