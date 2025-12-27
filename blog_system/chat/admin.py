from django.contrib import admin
from .models import ChatRoom, ChatMessage

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'participants_count']
    search_fields = ['name']
    def participants_count(self, obj):
        return obj.participants.count()
    participants_count.short_description = '参与人数'

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'room', 'content', 'created_at']
    list_filter = ['room', 'created_at']
    search_fields = ['content']