from rest_framework import serializers

from documents.models import Document, Folder
from users.models import CustomUser
from users.serializers import UserSerializer


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = "__all__"


class DocumentSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Document
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["sender"] = {"id": instance.sender.id, "username": instance.sender.username}

        # remove the signature before rendering the object
        ret.pop("signature")

        return ret

    def update(self, instance, validated_data):
        if instance.signature:
            validated_data.pop("signature", None)
        return super().update(instance, validated_data)
