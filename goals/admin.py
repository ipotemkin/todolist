from django.contrib import admin

from goals.models import GoalCategory, Goal, Comment, Board, BoardParticipant


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "board", "user", "created", "updated")
    search_fields = ("title", "user__username", "board__title")
    list_filter = ('is_deleted',)
    readonly_fields = ("created", "updated")


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "description", "due_date", "created", "updated")
    search_fields = ("title", "description", "category__title")
    list_filter = ('is_deleted',)
    readonly_fields = ("created", "updated")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "goal", "created", "updated")
    search_fields = ("text", "goal__title")
    readonly_fields = ("created", "updated")


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("title", "created", "updated")
    search_fields = ("title",)
    list_filter = ('is_deleted',)
    readonly_fields = ("created", "updated")


@admin.register(BoardParticipant)
class BoardParticipantAdmin(admin.ModelAdmin):
    list_display = ("user", "board", "role", "created", "updated")
    search_fields = ("user__username", "board__title")
    # list_filter = ('is_deleted',)
    readonly_fields = ("created", "updated")
