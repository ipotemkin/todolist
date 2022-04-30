from django.contrib import admin

from goals.models import GoalCategory, Goal, Comment


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")
    list_filter = ('is_deleted',)


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("category", "title", "description", "due_date", "created", "updated")
    search_fields = ("title", "description")
    list_filter = ('is_deleted',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("goal", "text", "created", "updated")
    search_fields = ("text", "goal__title")
