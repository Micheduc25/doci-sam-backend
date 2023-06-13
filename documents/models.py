from django.db import models
from users.models import CustomUser


class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "self", related_name="folders", null=True, blank=True, on_delete=models.SET_NULL
    )

    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]


class Document(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sender = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name="sent_documents"
    )
    receivers = models.ManyToManyField(
        CustomUser,
        related_name="received_documents",
    )
    file = models.FileField(upload_to="documents/%Y/%m/%d/", max_length=100)
    is_public = models.BooleanField(default=False)
    signature = models.TextField()

    folder = models.ForeignKey(
        Folder,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="documents",
    )

    class Meta:
        ordering = ["-created_at"]
