from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# 自定义User的后台显示
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'date_joined')
    search_fields = ('username', 'email')

admin.site.register(User, CustomUserAdmin)