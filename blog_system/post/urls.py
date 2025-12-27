# post/urls.py
from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.post_list, name='index'),
    path('about/', views.post_about, name='about'),
    path('post/<int:pk>/', views.post_detail, name='detail'),
    path('post/create/', views.post_create, name='create'),
    path('post/<int:pk>/update/', views.post_update, name='update'),
    path('post/<int:pk>/delete/', views.post_delete, name='delete'),
    path('post/<int:pk>/comment/', views.post_comment, name='comment'),
    # 新增分类接口路由
    path('category/create/', views.category_create, name='category_create'),
]