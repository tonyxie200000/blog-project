from django.db import models
from django.contrib.auth import get_user_model

# 获取Django默认的User模型
User = get_user_model()

class Category(models.Model):
    """文章分类模型"""
    name = models.CharField('分类名称', max_length=50, unique=True)
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='创建人'
    )
    is_deleted = models.BooleanField('是否删除', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def soft_delete(self):
        """软删除：标记为已删除，不物理删除"""
        self.is_deleted = True
        self.save()

    def restore(self):
        """恢复已删除的分类"""
        self.is_deleted = False
        self.save()


class Post(models.Model):
    """文章模型"""
    title = models.CharField('文章标题', max_length=200, unique=True)
    # 文章内容（TextField支持大文本）
    content = models.TextField('文章内容')
    # 关联分类（分类删除时，文章的category字段置空）
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',  # 反向关联：category.posts 可获取该分类下所有文章
        verbose_name='所属分类'
    )
    # 文章作者（作者删除时，关联的文章也删除）
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',  # 反向关联：user.posts 可获取该用户发布的所有文章
        verbose_name='作者'
    )
    # 阅读量（默认0，整数类型）
    views = models.PositiveIntegerField('阅读量', default=0)
    # 是否发布（草稿/已发布）
    is_published = models.BooleanField('是否发布', default=True)
    # 是否删除（软删除标记）
    is_deleted = models.BooleanField('是否删除', default=False)
    # 时间戳
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        # 排序：最新创建的文章在前
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def increase_views(self):
        """增加阅读量（每次访问文章详情页调用）"""
        self.views += 1
        # 只更新views字段，提高性能
        self.save(update_fields=['views'])

    def soft_delete(self):
        """软删除文章"""
        self.is_deleted = True
        self.save()

    def restore(self):
        """恢复已删除的文章"""
        self.is_deleted = False
        self.save()

    @property
    def category_name(self):
        """快捷获取分类名称（避免模板中判断None）"""
        return self.category.name if self.category else '未分类'


# 核心修正：Comment模型移出Post模型，作为独立模型
class Comment(models.Model):
    """文章评论模型"""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='所属文章'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='评论者'
    )
    content = models.TextField('评论内容')
    created_at = models.DateTimeField('评论时间', auto_now_add=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['-created_at']  # 最新评论在前

    def __str__(self):
        return f'{self.author.username} - {self.content[:20]}'