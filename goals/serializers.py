from rest_framework import serializers

from core.serializers import UserSerializer
from goals.models import GoalCategory, Goal, Comment


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalSerializer(serializers.ModelSerializer):
    # category = GoalCategorySerializer()
    # category_id = serializers.IntegerField(source='category.id')

    # def validate_category(self, value):
    #     if value.is_deleted:
    #         raise serializers.ValidationError("not allowed in deleted category")
    #
    #     if value.user != self.context["request"].user:
    #         raise serializers.ValidationError("not owner of category")
    #
    #     return value

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "category")


class GoalCreateSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated")
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    user = UserSerializer(source="goal.category.user", read_only=True)
    # print(user)
    # category = GoalCategorySerializer()
    # category_id = serializers.IntegerField(source='category.id')

    # def validate_category(self, value):
    #     if value.is_deleted:
    #         raise serializers.ValidationError("not allowed in deleted category")
    #
    #     if value.user != self.context["request"].user:
    #         raise serializers.ValidationError("not owner of category")
    #
    #     return value

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "goal")


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        read_only_fields = ("id", "created", "updated")
        fields = "__all__"
