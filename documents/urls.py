from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from documents.views import (
    DocumentViewSet,
    verifyDocument,
    search_documents,
    fetchFolderlessDocuments,
    fetchFolderDocuments,
    fetchSubfolders,
    fetchPublicFolders,
    FoldersAPIView,
)

from django.urls import path

router = routers.DefaultRouter()

router.register("documents", DocumentViewSet)


urlpatterns = [
    path("documents/verify/", verifyDocument),
    path("documents/search/", search_documents),
    path("documents/nofolder-documents/", fetchFolderlessDocuments),
    path("folders/", FoldersAPIView.as_view(), name="folders"),
    path("folders/<int:pk>/", FoldersAPIView.as_view(), name="folders-details"),
    path("folders/public/", fetchPublicFolders),
    path("folders/<int:folder>/documents/", fetchFolderDocuments),
    path("folders/<int:folder>/subfolders/", fetchSubfolders),
] + router.urls
