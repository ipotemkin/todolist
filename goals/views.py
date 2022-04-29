from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination

from goals.filters import GoalDataFilter
from goals.models import GoalCategory, Goal, Comment
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalSerializer, \
    GoalCreateSerializer, CommentSerializer, CommentCreateSerializer


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            user=self.request.user, is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_class = GoalDataFilter
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        return Goal.objects.filter(
            category__user=self.request.user,
            is_deleted=False
        )


class GoalCreateView(CreateAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(category__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class CommentListView(ListAPIView):
    # queryset = Comment.objects.all()
    model = Comment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        # filters.SearchFilter,
        DjangoFilterBackend,
    ]
    # filterset_class = GoalDataFilter
    ordering_fields = ["updated", "created"]
    ordering = ["-created", "updated"]
    # search_fields = ["=goal_id"]
    filterset_fields = ["goal"]

    def get_queryset(self):
        return Comment.objects.filter()


class CommentCreateView(CreateAPIView):
    model = Comment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentCreateSerializer


class CommentView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    model = Comment
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
