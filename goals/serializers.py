from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import PermissionDenied

from core.models import User
from core.serializers import UserSerializer
from goals.models import GoalCategory, Goal, Comment, Board, BoardParticipant


class CreatePermissionsModelSerializer(serializers.ModelSerializer):
    """To check permissions while creating objects"""

    # class Meta:
    #     model = None

    def create(self, validated_data):
        obj = self.Meta.model(**self.validated_data)
        view = self._context["view"]
        request = self._context["request"]
        for permission in view.permission_classes:
            if not permission.has_object_permission(self, request, view, obj):
                raise PermissionDenied
        return super().create(validated_data)


class GoalCategoryCreateSerializer(CreatePermissionsModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ["id", "created", "updated", "user"]
        fields = "__all__"


class GoalCategorySerializer(GoalCategoryCreateSerializer):
    user = UserSerializer(read_only=True)

    # проверить работу приложения – возможны ошибки с этой строчкой
    board = serializers.IntegerField(source="board_id", read_only=True)

    # user = serializers.IntegerField(source='user_id', read_only=True)

    def validate_user(self, value):
        if value != self.context["request"].user:
            raise ValidationError("not owner of category")
        return value

    def validate_is_deleted(self, value):
        if value:
            raise ValidationError("not allowed in deleted category")
        return value


# to speed up performance
class GoalCategoryReadSerializer(GoalCategoryCreateSerializer):
    user = UserSerializer(read_only=True)

    class Meta(GoalCategoryCreateSerializer.Meta):
        read_only_fields = ["id", "created", "updated", "user", "title", "board"]


# to speed up performance
class GoalCategoryReadSimpleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    user = serializers.IntegerField(source="user_id", read_only=True)
    board = serializers.IntegerField(source="board_id", read_only=True)
    is_deleted = serializers.BooleanField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)


class GoalCreateSerializer(CreatePermissionsModelSerializer):
    class Meta:
        model = Goal
        read_only_fields = ["id", "created", "updated"]
        fields = "__all__"

    def validate_category(self, value):
        if value.is_deleted:
            raise ValidationError("not allowed in deleted category")
        return value


class GoalSerializer(GoalCreateSerializer):
    board = serializers.IntegerField(source="category.board_id", read_only=True)

    class Meta(GoalCreateSerializer.Meta):
        read_only_fields = ["id", "created", "updated", "category"]

    def validate_is_deleted(self, value):
        if value:
            raise ValidationError("not allowed on deleted goal")
        return value


class CommentCreateSerializer(CreatePermissionsModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        read_only_fields = ["id", "created", "updated"]
        fields = "__all__"

    def validate_goal(self, value):
        if value.is_deleted:
            raise ValidationError("not allowed on deleted goal")
        return value


class CommentSerializer(CommentCreateSerializer):
    user = UserSerializer(read_only=True)

    class Meta(CommentCreateSerializer.Meta):
        read_only_fields = ["id", "created", "updated", "goal"]


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated")
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=BoardParticipant.Role.owner
        )
        return board


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(required=True, choices=BoardParticipant.Role.choices)
    user = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")

    def update(self, instance, validated_data):
        # owner = validated_data.pop("user")
        owner = self.context["request"].user
        new_participants = validated_data.pop("participants", [])
        new_by_id = {part["user"].id: part for part in new_participants}

        old_participants = instance.participants.exclude(user=owner)
        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user_id not in new_by_id:
                    old_participant.delete()
                else:
                    if (
                        old_participant.role
                        != new_by_id[old_participant.user_id]["role"]
                    ):
                        old_participant.role = new_by_id[old_participant.user_id][
                            "role"
                        ]
                        old_participant.save()
                    new_by_id.pop(old_participant.user_id)
            for new_part in new_by_id.values():
                BoardParticipant.objects.create(
                    board=instance, user=new_part["user"], role=new_part["role"]
                )

            if "title" in validated_data:
                instance.title = validated_data["title"]
            instance.save()

        return instance


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"
