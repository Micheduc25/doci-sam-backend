from rest_framework import permissions


class IsSenderOrReceiver(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the object.
        if request.method in permissions.SAFE_METHODS:
            return request.user == obj.sender or request.user.id in map(
                lambda u: u["id"], obj.receivers.values()
            )

        return False


class IsSenderOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True

        if request.user == obj.sender:
            return True

        return False


class IsPublicDocument(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the object.
        return obj.is_public
