from django.contrib import admin
from users.models import CustomUser
from documents.models import Document, Folder

admin.site.register(CustomUser)

admin.site.register(Folder)


class FolderAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name"]


admin.site.site_title = "Document Manager"
admin.site.site_header = "Document Manager"


admin.site.register(Document)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["title", "description"]
