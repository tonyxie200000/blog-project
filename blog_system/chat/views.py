from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .models import ChatRoom, ChatMessage
from .forms import ChatMessageForm, ChatRoomForm


# 聊天房间列表（优化：仅显示用户加入的房间）
@login_required
def chat_index(request):
    # 只显示当前用户加入的房间，更合理
    rooms = request.user.chat_rooms.all().order_by('-created_at')
    return render(request, 'chat/index.html', {'rooms': rooms})


# 聊天房间详情（优化：异常捕获+消息校验）
@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)

    # 自动加入房间（优化：防重复添加）
    if request.user not in room.participants.all():
        room.participants.add(request.user)
        messages.success(request, f'成功加入房间：{room.name}')

    # 发送消息（优化：异常处理）
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            try:
                msg = form.save(commit=False)
                msg.room = room
                msg.sender = request.user
                msg.save()
                return redirect('chat:room', room_id=room.id)
            except ValueError as e:
                messages.error(request, f'发送失败：{str(e)}')
            except IntegrityError:
                messages.error(request, '发送失败：数据异常，请重试！')
        else:
            messages.error(request, '消息内容不能为空！')

    # 加载消息和表单
    form = ChatMessageForm()
    messages_list = ChatMessage.objects.filter(room=room).order_by('created_at')
    return render(request, 'chat/room.html', {
        'room': room,
        'form': form,
        'messages': messages_list
    })


# 创建聊天房间（优化：表单校验+异常捕获）
@login_required
def chat_room_create(request):
    if request.method == 'POST':
        form = ChatRoomForm(request.POST)
        if form.is_valid():
            try:
                room = form.save()
                room.participants.add(request.user)
                messages.success(request, '聊天房间创建成功！')
                return redirect('chat:room', room_id=room.id)
            except IntegrityError:
                messages.error(request, '创建失败：房间名称已存在！')
            except Exception as e:
                messages.error(request, f'创建失败：{str(e)}')
    else:
        form = ChatRoomForm()
    return render(request, 'chat/room_create.html', {'form': form})