from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    GenericAPIView,
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.filters import GoalDataFilter
from goals.models import GoalCategory, Goal, Comment, Board
from goals.permissions import (
    BoardPermissions,
    GoalCategoryPermissions,
    GoalPermissions,
    CommentPermissions,
    CommentCreatePermissions,
)
from goals.serializers import (
    GoalCategoryCreateSerializer,
    GoalCategorySerializer,
    GoalSerializer,
    GoalCreateSerializer,
    CommentSerializer,
    CommentCreateSerializer,
    BoardSerializer,
    BoardListSerializer,
    BoardCreateSerializer,
    GoalCategoryReadSerializer,
    # GoalCategoryReadSimpleSerializer
)

# from time import perf_counter


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = (IsAuthenticated, GoalCategoryPermissions)
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryMixin(GenericAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = (IsAuthenticated, GoalCategoryPermissions)

    def get_queryset(self):
        query = Q(board__participants__user__username=self.request.user) & Q(
            is_deleted=False
        )
        return (
            GoalCategory.objects
            # .prefetch_related('board', 'user')  # 5 queries
            # .select_related('board', 'user')  # 3 queries
            .select_related("user").filter(query)  # 3 queries  # 13 queries
        )
        # количество запросов оптимизировано с 13 до 3


class GoalCategoryListView(ListAPIView, GoalCategoryMixin):
    serializer_class = GoalCategoryReadSerializer
    # serializer_class = GoalCategoryReadSimpleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (
        OrderingFilter,
        SearchFilter,
        DjangoFilterBackend,
    )
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]
    filterset_fields = ["board"]

    # def list(self, request, *args, **kwargs):
    #     start = perf_counter()
    #     ret = super().list(request, *args, **kwargs)
    #     elapsed = perf_counter() - start
    #     print('Время выполнения: [%0.8fs]' % elapsed)
    #     return ret


class GoalCategoryView(RetrieveUpdateDestroyAPIView, GoalCategoryMixin):
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        instance.goals.update(is_deleted=True)
        return instance


class GoalCreateView(CreateAPIView):
    model = Goal
    permission_classes = (IsAuthenticated, GoalPermissions)
    serializer_class = GoalCreateSerializer


class GoalMixin(GenericAPIView):
    model = Goal
    permission_classes = (IsAuthenticated, GoalPermissions)
    serializer_class = GoalSerializer

    def get_queryset(self):
        return Goal.objects.select_related("category").filter(  # 3 queries
            category__board__participants__user__username=self.request.user,
            is_deleted=False,
        )  # 15 queries
        # количество запросов оптимизировано с 15 до 3


class GoalListView(ListAPIView, GoalMixin):
    pagination_class = LimitOffsetPagination
    filter_backends = (
        OrderingFilter,
        SearchFilter,
        DjangoFilterBackend,
    )
    filterset_class = GoalDataFilter
    ordering_fields = ["priority", "due_date"]
    ordering = ["-priority", "due_date"]
    search_fields = ["title", "description"]


class GoalView(RetrieveUpdateDestroyAPIView, GoalMixin):
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class CommentCreateView(CreateAPIView):
    model = Comment
    permission_classes = (IsAuthenticated, CommentCreatePermissions)
    serializer_class = CommentCreateSerializer


class CommentMixin(GenericAPIView):
    model = Comment
    permission_classes = (IsAuthenticated, CommentPermissions)
    serializer_class = CommentSerializer

    def get_queryset(self):
        return (
            Comment.objects
            # .select_related('goal')  # 14 queries
            # .select_related('user')  # 13 queries
            # 12 queries
            .select_related("user")
            .select_related("goal__category__board")
            .all()  # 14 queries
        )
        # Количество запросов было оптимизировано с 14 до 12,
        # после замены board на board_id в permissions
        # количество запросов удалось сократить до 10.
        # Это количество запросов при открытии списка комментариев цели через фронт.
        # Итоговое количество запросов большое в связи с тем,
        # что фронт делает аж 3 запроса к api
        # Соответственно, если запрашивать через api только список комментариев,
        # количество запросов к БД будет меньше (должно быть 4 запроса)


class CommentListView(ListAPIView, CommentMixin):
    pagination_class = LimitOffsetPagination
    filter_backends = (
        OrderingFilter,
        DjangoFilterBackend,
    )
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
    permission_classes = (IsAuthenticated, BoardPermissions)
    serializer_class = BoardSerializer

    def get_queryset(self):
        # эта строчка вызывала ошибку в swagger
        # return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

        # после добавления id ошибка исчезла => нужно протестить
        return Board.objects.filter(
            participants__user=self.request.user.id, is_deleted=False
        )


class BoardView(RetrieveUpdateDestroyAPIView, BoardMixin):
    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(is_deleted=True)
        return instance


class BoardListView(ListAPIView, BoardMixin):
    serializer_class = BoardListSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (OrderingFilter,)
    ordering_fields = ("title",)
    ordering = ("title",)
