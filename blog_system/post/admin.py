from django.contrib import admin
from .models import Category, Post

# 文章分类后台
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'is_deleted')
    search_fields = ('name',)

# 文章后台
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'views', 'is_published')
    list_filter = ('category', 'is_published', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('views', 'created_at', 'updated_at')