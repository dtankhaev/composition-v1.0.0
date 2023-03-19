from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    """Разрешение на доступ к пользователям."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(BasePermission):
    """Разрешение для ресурса Жанров,
    Категорий и Произведений.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_admin
            )
        )


class AuthorAndStaffOrReadOnly(BasePermission):
    """Разрешение для отзывов и комментариев."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_moderator or request.user.is_admin
            or request.user == obj.author
        )
