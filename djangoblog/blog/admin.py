from django.contrib import admin
from .models import Post, Comment, Category


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "created_at"]
    search_fields = ["title", "content"]
    list_filter = ["created_at", "category"]
    ordering = ["-created_at"]
    inlines = [CommentInline]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["author", "post", "created_at"]
    search_fields = ["author", "text"]
    list_filter = ["created_at", "post"]
    ordering = ["-created_at"]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
