from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models.query import Q

from rest_framework import exceptions

from documents.models import Document, Folder
from documents.serializers import DocumentSerializer, FolderSerializer
from rest_framework.views import APIView
from rest_framework import exceptions

from .permissions import IsSenderOrReceiver, IsPublicDocument, IsSenderOrAdmin


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if self.request.GET.get("public") == "true":
            return Document.objects.filter(is_public=True)

        elif self.request.GET.get("shared") == "true":
            queryset = Document.objects.filter(receivers=user)

            return queryset.distinct()

        queryset = Document.objects.filter(Q(sender=user) | Q(receivers=user))

        return queryset.distinct()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [IsSenderOrReceiver | IsPublicDocument]

        elif self.action in ["update", "destroy"]:
            permission_classes = [IsSenderOrAdmin]

        else:
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def verifyDocument(request):
    if request.data["signature"] is None:
        return exceptions.ValidationError("No signature was provided")

    signature = request.data.get("signature")
    document_id = request.data.get("document_id")

    try:
        document = Document.objects.get(pk=document_id)

        if document.signature == signature:
            return exceptions.JsonResponse({"is_authentic": True})

        else:
            return exceptions.JsonResponse({"is_authentic": False})
    except Document.DoesNotExist:
        return Response("this document does not exist", status=404)


class FoldersAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user_folders = Folder.objects.filter(creator=self.request.user)

            folder_serializer = FolderSerializer(user_folders, many=True)

            return Response(folder_serializer.data)

        except Folder.DoesNotExist:
            return Response("No folder was found", status=404)

    def post(self, request):
        data = self.request.data

        folder_serializer = FolderSerializer(data=data)

        try:
            folder_serializer.is_valid(raise_exception=True)

            folder_serializer.save()

            return Response(folder_serializer.data)
        except Exception:
            return exceptions.ValidationError()
