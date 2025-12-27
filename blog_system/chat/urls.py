from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_index, name='index'),          # 房间列表
    path('room/create/', views.chat_room_create, name='room_create'),  # 创建房间
    path('room/<int:room_id>/', views.chat_room, name='room'),  # 房间详情
]