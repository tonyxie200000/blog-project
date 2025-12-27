from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """自定义用户模型，仅继承AbstractUser，无额外字段"""
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'