
# Register your models here.
from django.contrib import admin
from replies.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('tweet', 'user', 'content', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'