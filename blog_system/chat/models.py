from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatRoom(models.Model):
    """聊天房间模型（优化：增加字符串友好展示）"""
    name = models.CharField('房间名称', max_length=100, unique=True)
    description = models.TextField('房间描述', blank=True, null=True)
    participants = models.ManyToManyField(
        User,
        related_name='chat_rooms',
        verbose_name='参与者'
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '聊天房间'
        verbose_name_plural = '聊天房间'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def participant_count(self):
        """快捷获取参与人数（模板中可直接用）"""
        return self.participants.count()


class ChatMessage(models.Model):
    """聊天消息模型（核心优化：兼容空值+防呆）"""
    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='所属房间',
        null=True,  # 兼容旧数据，避免迁移报错
        blank=True  # 表单层允许空值，视图层强制赋值
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name='发送者'
    )
    content = models.TextField('消息内容')
    created_at = models.DateTimeField('发送时间', auto_now_add=True)

    class Meta:
        verbose_name = '聊天消息'
        verbose_name_plural = '聊天消息'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender.username}: {self.content[:20]}'

    def save(self, *args, **kwargs):
        """重写保存方法：强制校验房间非空（视图层兜底）"""
        if not self.room:
            raise ValueError("聊天消息必须关联到具体房间！")
        super().save(*args, **kwargs)