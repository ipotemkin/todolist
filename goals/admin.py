from django.contrib import admin

from goals.models import GoalCategory, Goal, Comment


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")


class GoalAdmin(admin.ModelAdmin):
    list_display = ("category", "title", "description", "due_date", "created", "updated")
    search_fields = ("title", "description")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("goal", "text", "created", "updated")
    search_fields = ("text", "goal__title")


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Comment, CommentAdmin)
