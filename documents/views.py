from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models.query import Q
from rest_framework.request import Request

from rest_framework import exceptions

from documents.models import Document, Folder
from documents.serializers import DocumentSerializer, FolderSerializer
from rest_framework.views import APIView
from rest_framework import exceptions

from .permissions import IsSenderOrReceiver, IsPublicDocument, IsSenderOrAdmin
from users.permissions import IsActiveUser
from django.shortcuts import get_object_or_404, get_list_or_404


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        print(context)
        return context

    def get_queryset(self):
        user = self.request.user

        if self.request.GET.get("public") == "true":
            return Document.objects.filter(is_public=True)

        elif self.request.GET.get("shared") == "true":
            queryset = Document.objects.filter(receivers=user)

            return queryset.distinct()

        queryset = Document.objects.filter(Q(sender=user) | Q(receivers=user))

        return queryset.distinct()

    def perform_create(self, serializer):
        receivers = self.request.data.getlist("receivers[]")
        serializer.save(receivers=receivers)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.get_queryset(), many=True, context={"request": request}
        )
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={"request": request})
        return Response(serializer.data)

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

    def get(self, request: Request, pk=None):
        if pk is None:
            user_folders = Folder.objects.filter(
                Q(creator=self.request.user) & Q(parent=None)
            )

            folder_serializer = FolderSerializer(user_folders, many=True)

            return Response(folder_serializer.data)

        else:
            folder = get_object_or_404(Folder, pk=pk)
            data = FolderSerializer(folder).data
            return Response(data)

    def post(self, request):
        data = self.request.data

        folder_serializer = FolderSerializer(data=data, context={"request": request})

        folder_serializer.is_valid(raise_exception=True)

        folder_serializer.save()

        folder_data = folder_serializer.data

        # if folder_data["parent"] is not None:
        #     print(folder_data["parent"])

        #     parent_serializer = FolderSerializer(data=folder_data["parent"])

        #     parent_serializer.is_valid(raise_exception=True)

        #     folder_data["parent"] = parent_serializer.data

        return Response(folder_data)

    def put(self, request, pk):
        print(pk)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def fetchFolderlessDocuments(request):
    user = request.user

    try:
        documents = Document.objects.filter(Q(sender=user) & Q(folder=None))

        serializer = DocumentSerializer(
            documents, many=True, context={"request": request}
        )

        return Response(serializer.data)
    except Document.DoesNotExist:
        return Response("No matching documents found", status=404)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def fetchFolderDocuments(request, folder):
    try:
        documents = Document.objects.filter(folder=folder)

        serializer = DocumentSerializer(
            documents, many=True, context={"request": request}
        )

        return Response(serializer.data)

    except Folder.DoesNotExist:
        return Response("No matching folder found", status=404)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def fetchPublicFolders(request):
    folders = get_list_or_404(Folder.objects.filter(is_public=True))

    data = FolderSerializer(folders, many=True).data
    return Response(data)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def fetchAllFolders(request):
    folders = Folder.objects.filter(creator=request.user)

    data = FolderSerializer(folders, many=True).data
    return Response(data)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def fetchSubfolders(request, folder):
    try:
        subfolders = Folder.objects.filter(Q(parent=folder) & Q(creator=request.user))
        serializer = FolderSerializer(subfolders, many=True)
        return Response(serializer.data)
    except Folder.DoesNotExist:
        return Response("No matching subfolders found", status=404)


@api_view(["POST"])
# @permission_classes([permissions.IsAuthenticated])
def search_documents(request):
    if (
        len(request.data.keys()) == 0
        or "keyword" not in request.data.keys()
        or request.data["keyword"] is None
    ):
        return Response("No keyword was provided", status=400)

    keyword = request.data["keyword"]

    try:
        matching_documents = Document.objects.filter(
            Q(title__icontains=keyword) | Q(description__icontains=keyword)
        )

        doc_serializer = DocumentSerializer(
            matching_documents, many=True, context={"request": request}
        )

        return Response(doc_serializer.data)
    except Document.DoesNotExist:
        return Response("No matching document was found", status=404)
