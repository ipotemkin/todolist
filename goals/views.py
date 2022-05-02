from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.filters import GoalDataFilter
from goals.models import GoalCategory, Goal, Comment, Board
from goals.permissions import BoardPermissions, GoalCategoryPermissions
from goals.serializers import (
    GoalCategoryCreateSerializer,
    GoalCategorySerializer,
    GoalSerializer,
    GoalCreateSerializer,
    CommentSerializer,
    CommentCreateSerializer, BoardSerializer, BoardListSerializer, BoardCreateSerializer
)


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [IsAuthenticated, GoalCategoryPermissions]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryMixin(GenericAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [IsAuthenticated, GoalCategoryPermissions]

    def get_queryset(self):
        query = (
                # Q(user=self.request.user) |
                Q(board__participants__user__username=self.request.user)
        ) & Q(is_deleted=False)
        return GoalCategory.objects.filter(
            # user=self.request.user,
            # is_deleted=False,
            query
        )


class GoalCategoryListView(ListAPIView, GoalCategoryMixin):
    pagination_class = LimitOffsetPagination
    filter_backends = [
        OrderingFilter,
        SearchFilter,
        DjangoFilterBackend,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]
    filterset_fields = ["board"]


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
            # category__user=self.request.user,
            category__board__participants__user__username=self.request.user,
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
    ordering_fields = ["priority", "due_date"]
    ordering = ["-priority", "due_date"]
    search_fields = ["title", "description"]
    # filterset_fields = ["category__in"]


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


class BoardCreateView(CreateAPIView):
    model = Board
    permission_classes = [IsAuthenticated]
    serializer_class = BoardCreateSerializer


class BoardMixin(GenericAPIView):
    model = Board
    permission_classes = [IsAuthenticated, BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        # Обратите внимание на фильтрацию – она идет через participants
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)


class BoardView(RetrieveUpdateDestroyAPIView, BoardMixin):
    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                # status=Goal.Status.archived
                is_deleted=True
            )
        return instance


class BoardListView(ListAPIView, BoardMixin):
    serializer_class = BoardListSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        OrderingFilter,
        # DjangoFilterBackend,
    ]
    ordering_fields = ("title",)
    ordering = ("title",)
    # filterset_fields = ["goal"]
