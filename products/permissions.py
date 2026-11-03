from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsModerator(BasePermission):
    """Allow staff moderators every product action except creation."""

    message = "Модератор может работать с продуктами, но не может создавать их."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
            and request.method != "POST"
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class CanCreateProduct(BasePermission):
    message = "Сотрудникам и модераторам запрещено создавать продукты."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and not request.user.is_staff
        )


class IsOwnerOrModerator(BasePermission):
    message = "Изменять и удалять продукт может владелец или модератор."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if obj.owner_id == request.user.id:
            return True
        return IsModerator().has_object_permission(request, view, obj)
