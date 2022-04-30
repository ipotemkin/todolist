from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.filters import GoalDataFilter
from goals.models import GoalCategory, Goal, Comment
from goals.serializers import (
    GoalCategoryCreateSerializer,
    GoalCategorySerializer,
    GoalSerializer,
    GoalCreateSerializer,
    CommentSerializer,
    CommentCreateSerializer
)


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryMixin(GenericAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            user=self.request.user,
            is_deleted=False,
        )


class GoalCategoryListView(ListAPIView, GoalCategoryMixin):
    pagination_class = LimitOffsetPagination
    filter_backends = [
        OrderingFilter,
        SearchFilter,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]


class GoalCategoryView(RetrieveUpdateDestroyAPIView, GoalCategoryMixin):
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class GoalCreateView(CreateAPIView):
    model = Goal
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalMixin(GenericAPIView):
    model = Goal
    permission_classes = [IsAuthenticated]
    serializer_class = GoalSerializer

    def get_queryset(self):
        return Goal.objects.filter(
            category__user=self.request.user,
            is_deleted=False
        )


class GoalListView(ListAPIView, GoalMixin):
    pagination_class = LimitOffsetPagination
    filter_backends = [
        OrderingFilter,
        SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_class = GoalDataFilter
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title", "description"]


class GoalView(RetrieveUpdateDestroyAPIView, GoalMixin):
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class CommentCreateView(CreateAPIView):
    model = Comment
    permission_classes = [IsAuthenticated]
    serializer_class = CommentCreateSerializer


class CommentMixin(GenericAPIView):
    model = Comment
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(goal__category__user=self.request.user)


class CommentListView(ListAPIView, CommentMixin):
    pagination_class = LimitOffsetPagination
    filter_backends = [
        OrderingFilter,
        DjangoFilterBackend,
    ]
    ordering_fields = ("created", "updated")
    ordering = ("-created",)
    filterset_fields = ["goal"]


class CommentView(RetrieveUpdateDestroyAPIView, CommentMixin):
    pass
