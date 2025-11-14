from rest_framework import permissions

class IsInstructor(permissions.BasePermission):
    """
    Allows access only to users with role 'instructor'.
    """

    def has_permission(self, request, view):
        return bool(
            request.user 
            and request.user.is_authenticated 
            and request.user.role == 'instructor'
        )

class IsStudent(permissions.BasePermission):
    """
    Allows access only to users with role 'student'.
    Useful for enrollment actions.
    """

    def has_permission(self, request, view):
        return bool(
            request.user 
            and request.user.is_authenticated 
            and request.user.role == 'student'
        )
