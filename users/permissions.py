from rest_framework import permissions


class IsCurrentUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return super().has_object_permission(request, view, obj)

        else:
            return request.user.id == obj.id
