from rest_framework.permissions import BasePermission


class IsProjectOwnerPermission(BasePermission):
    """Permission class for Project View"""

    def has_object_permission(self, request, view, obj):
        """Object level permission to check that requested user is object owner or not"""

        if request.method in ["PUT", "PATCH", "DELETE"]:
            return request.user == obj.created_by

        return True


class IsTimeLogOwnerPermission(BasePermission):
    """Permission class for Time Log View"""

    def has_object_permission(self, request, view, obj):
        """Object level permission to check that requested user is object owner or not"""

        if request.method in ["PUT", "PATCH", "DELETE"]:
            return request.user == obj.user

        return True
