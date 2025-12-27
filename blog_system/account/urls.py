from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
app_name = 'account'  # 命名空间
urlpatterns = [
    path('login/', views.user_login, name='login'),   # 登录
    path('logout/', views.user_logout, name='logout'), # 登出
    path('register/', views.user_register, name='register'), # 注册
]