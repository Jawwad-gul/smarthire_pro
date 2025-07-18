from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsEmployerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (
            request.user and request.user.is_authenticated and request.user.is_employer
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.posted_by == request.user
