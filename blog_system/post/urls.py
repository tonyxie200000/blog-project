# post/urls.py
from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.post_list, name='index'),
    path('about/', views.post_about, name='about'),
    # post/urls.py
    path('post/<int:pk>/', views.post_detail, name='post_detail'),  # 原name='detail'改为name='post_detail'
    path('post/create/', views.post_create, name='create'),
    path('post/<int:pk>/update/', views.post_update, name='update'),
    path("post/<int:pk>/edit/", views.post_edit, name="edit"),  # 编辑
    path("post/<int:pk>/delete/", views.post_delete, name="delete"),  # 删除
    path('post/<int:pk>/comment/', views.post_comment, name='comment'),
    # 新增分类接口路由
    path('category/create/', views.category_create, name='category_create'),
    # 新增：按分类筛选文章
    path("category/<int:category_id>/", views.post_by_category, name="post_by_category"),
    path('post/publish/', views.post_publish, name='post_publish'),
    path("my-posts/", views.my_posts, name="my_posts"),
    path("detail/<int:pk>/", views.post_detail, name="post_detail"),

    ]
