from django.db import models
from django.conf import settings  # 新增导入
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """自定义用户模型，仅继承AbstractUser，无额外字段"""
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='account_user_groups',  # 唯一命名
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='account_user_permissions',  # 唯一命名
        blank=True
    )
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

class UserProfile(models.Model):
        # 与Django内置User关联（一对一）
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
        # 个人资料字段（可自定义）
    nickname = models.CharField(max_length=50, blank=True, verbose_name="昵称")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="头像")
    bio = models.TextField(blank=True, verbose_name="个人简介")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

# 信号：创建User时自动创建UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Profile(models.Model):
    # 添加related_name参数，比如设为"user_profile"
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    nickname = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
