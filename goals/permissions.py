from django.db.models import Q
from rest_framework import permissions

from goals.models import BoardParticipant


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user,
                board=obj
            ).exists()

        return BoardParticipant.objects.filter(
            user=request.user,
            board=obj,
            role=BoardParticipant.Role.owner
        ).exists()


class GoalCategoryPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            print('request.method =', request.method)
            return BoardParticipant.objects.filter(
                user=request.user,
                board=obj.board
            ).exists()

        print("unsafe methods")
        query = (
                    (Q(role=BoardParticipant.Role.owner) | Q(role=BoardParticipant.Role.writer))
                    & Q(user=request.user)
                    & Q(board=obj.board)
        )
        return BoardParticipant.objects.filter(query).exists()
