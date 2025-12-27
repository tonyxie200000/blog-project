from django.contrib import admin
from .models import Category, Post, Comment  # 新增Comment（匹配新models.py）

# 文章分类后台（移除不存在的is_deleted字段）
class CategoryAdmin(admin.ModelAdmin):
    # 原list_display中的is_deleted不存在，替换为models中有的updated_at
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)  # 保留你原本的搜索配置

# 文章后台（移除不存在的views字段）
class PostAdmin(admin.ModelAdmin):
    # 原list_display中的views不存在，删除该字段
    list_display = ('title', 'author', 'category', 'created_at', 'is_published')
    list_filter = ('category', 'is_published', 'created_at')  # 保留你原本的筛选配置
    search_fields = ('title', 'content')  # 保留你原本的搜索配置
    # 原readonly_fields中的views不存在，删除该字段
    readonly_fields = ('created_at', 'updated_at')

# 新增：评论后台（匹配新models.py的Comment模型）
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'content', 'created_at')
    list_filter = ('post', 'created_at')

# 注册模型（保留你原本的注册方式，新增Comment）
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
