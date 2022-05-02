from django.db.models import Q
from rest_framework import permissions

from goals.models import BoardParticipant


EDITABLE_ROLES = Q(role=BoardParticipant.Role.owner) | Q(role=BoardParticipant.Role.writer)


def check_user_board_permissions(request, board, required_roles: Q) -> bool:
    """A shortcut to check the 'request.user's permissions on the specified board."""

    if not request.user.is_authenticated:
        return False

    query = Q(user=request.user) & Q(board=board)

    if request.method not in permissions.SAFE_METHODS:
        query &= required_roles

    return BoardParticipant.objects.filter(query).exists()


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        return check_user_board_permissions(request, obj, Q(role=BoardParticipant.Role.owner))


class GoalCategoryPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        return check_user_board_permissions(request, obj.board, EDITABLE_ROLES)


class GoalPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        return check_user_board_permissions(request, obj.category.board, EDITABLE_ROLES)


class CommentPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:

        # изменяет/удаляет комментарий только его автор
        if obj.user != request.user:
            return False

        # автор может изменить/удалить свой комментарий только если на этой доске у него роль owner/writer
        return check_user_board_permissions(request, obj.goal.category.board, EDITABLE_ROLES)


class CommentCreatePermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        return check_user_board_permissions(request, obj.goal.category.board, EDITABLE_ROLES)
