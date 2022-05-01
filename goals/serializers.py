from rest_framework import serializers
from rest_framework.serializers import ValidationError

from core.serializers import UserSerializer
from goals.models import GoalCategory, Goal, Comment, Board, BoardParticipant


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCategorySerializer(GoalCategoryCreateSerializer):
    user = UserSerializer(read_only=True)

    def validate_user(self, value):
        if value != self.context["request"].user:
            raise ValidationError("not owner of category")
        return value

    def validate_is_deleted(self, value):
        if value:
            raise ValidationError("not allowed in deleted category")
        return value


class GoalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated")
        fields = "__all__"

    def validate_category(self, value):
        if value.is_deleted:
            raise ValidationError("not allowed in deleted category")
        if value.user != self.context["request"].user:
            raise ValidationError("not owner of category")
        return value


class GoalSerializer(GoalCreateSerializer):
    class Meta(GoalCreateSerializer.Meta):
        read_only_fields = ("id", "created", "updated", "category")

    def validate_is_deleted(self, value):
        if value:
            raise ValidationError("not allowed on deleted goal")
        return value


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        read_only_fields = ("id", "created", "updated")
        fields = "__all__"

    def validate_goal(self, value):
        if value.category.user != self.context["request"].user:
            raise ValidationError("not owner")
        if value.is_deleted:
            raise ValidationError("not allowed on deleted goal")
        return value


class CommentSerializer(CommentCreateSerializer):
    user = UserSerializer(source="goal.category.user", read_only=True)

    class Meta(CommentCreateSerializer.Meta):
        read_only_fields = ("id", "created", "updated", "goal")


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
