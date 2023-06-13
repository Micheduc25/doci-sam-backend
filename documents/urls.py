from rest_framework import routers

from documents.views import DocumentViewSet, verifyDocument, FoldersAPIView

from django.urls import path

router = routers.DefaultRouter()

router.register("documents", DocumentViewSet)


urlpatterns = [
    path("documents/verify/", verifyDocument),
    path("folders/", FoldersAPIView.as_view(), name="folders"),
] + router.urls
