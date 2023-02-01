from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsSelectionOwner(BasePermission):
    message = 'Нельзя редактировать чужие подборки'

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False


class IsAdOwnerOrStaff(BasePermission):
    message = 'У Вас нет доступа к этому объявлению'

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author or request.user.role in [UserRoles.MODERATOR or UserRoles.ADMIN]:
            return True
        return False
