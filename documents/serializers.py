from rest_framework import serializers

from documents.models import Document, Folder
from users.models import CustomUser
from users.serializers import UserSerializer


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = "__all__"
        depth = 10

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["creator"] = user

        parent_id = self.context["request"].data["parent"]

        if parent_id is not None:
            parent = Folder.objects.get(pk=parent_id)

            validated_data["parent"] = parent

        folder = Folder.objects.create(**validated_data)

        return folder

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        creator = instance.creator
        parent = instance.parent

        rep["creator"] = {
            "id": creator.id,
            "username": creator.username,
            "first_name": creator.first_name,
            "last_name": creator.last_name,
        }

        return rep


class DocumentSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    receivers = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), many=True
    )

    class Meta:
        model = Document
        fields = "__all__"

    def create(self, validated_data):
        if validated_data["is_public"] == True:
            return super().create(validated_data)

        if validated_data["receivers"] is None or len(validated_data["receivers"]) == 0:
            raise serializers.ValidationError("No receivers were specified")

        receivers = validated_data.pop("receivers")

        document = Document.objects.create(**validated_data)

        document.receivers.set(receivers)
        return document

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["sender"] = {"id": instance.sender.id, "username": instance.sender.username}

        if ret["folder"] is not None:
            try:
                folder = Folder.objects.get(pk=ret["folder"])
                ret["folder"] = FolderSerializer(folder).data
            except Folder.DoesNotExist:
                pass

        user = self.context["request"].user

        if user.id != instance.sender.id:
            # remove the signature before rendering the object
            ret.pop("signature")

        return ret

    def update(self, instance, validated_data):
        if instance.signature:
            validated_data.pop("signature", None)
        return super().update(instance, validated_data)
