# post/models.py 完整版本（包含文章、分类、评论，无导入错误）
from django.db import models
from django.conf import settings  # 关联Django内置用户模型
from django.utils import timezone

# 1. 文章分类模型（可选但实用）
class Category(models.Model):
    name = models.CharField(
        max_length=100, 
        verbose_name="分类名称",
        help_text="输入文章分类，如：技术、生活、随笔"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="创建时间"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="更新时间"
    )

    class Meta:
        verbose_name = "文章分类"       # 后台显示的单名
        verbose_name_plural = "文章分类" # 后台显示的复数名
        ordering = ["-created_at"]       # 按创建时间倒序排列

    def __str__(self):
        # 后台列表显示分类名，而非默认的Category object
        return self.name

# 2. 核心文章模型（解决普通用户发表权限）
class Post(models.Model):

    # 新增阅读量字段
    views = models.PositiveIntegerField(default=0, verbose_name="阅读量")
    
    # 新增increase_views方法
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    title = models.CharField(
        max_length=200, 
        verbose_name="文章标题",
        help_text="标题长度不超过200字"
    )
    content = models.TextField(
        verbose_name="文章内容",
        help_text="支持纯文本/HTML格式"
    )
    # 关联作者（普通用户/超级用户均可）
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # 作者删除，文章也删除
        verbose_name="文章作者",
        related_name="posts"       # 反向查询：user.posts 查看该用户所有文章
    )
    # 关联分类（可选，分类删除则置空）
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        verbose_name="文章分类",
        related_name="posts"
    )
    # 发布状态（默认发布）
    is_published = models.BooleanField(
        default=True, 
        verbose_name="是否发布",
        help_text="取消勾选则仅自己可见"
    )
    # 时间字段（自动生成）
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="创建时间"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="更新时间"
    )

    class Meta:
        verbose_name = "博客文章"
        verbose_name_plural = "博客文章"
        ordering = ["-created_at"]  # 新文章在前

    def __str__(self):
        # 后台列表显示“标题 - 作者”
        return f"{self.title} - {self.author.username}"

    # 可选：自定义方法（比如获取摘要）
    def get_excerpt(self):
        """返回文章前100字摘要"""
        if len(self.content) > 100:
            return self.content[:100] + "..."
        return self.content

# 3. 评论模型（解决views.py中Comment导入错误）
class Comment(models.Model):
    # 关联文章（文章删除，评论也删除）
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE,
        verbose_name="关联文章",
        related_name="comments"  # 反向查询：post.comments 查看该文章所有评论
    )
    # 关联评论者
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="评论者"
    )
    # 评论内容
    content = models.TextField(
        verbose_name="评论内容",
        help_text="请勿发布违规内容"
    )
    # 时间字段
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="评论时间"
    )

    class Meta:
        verbose_name = "文章评论"
        verbose_name_plural = "文章评论"
        ordering = ["-created_at"]  # 新评论在前

    def __str__(self):
        return f"{self.author.username} 评论《{self.post.title}》"
