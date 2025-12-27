from django import forms
from .models import ChatRoom, ChatMessage


class ChatRoomForm(forms.ModelForm):
    """创建房间表单（优化：样式+校验）"""

    class Meta:
        model = ChatRoom
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例如：技术交流群、好友闲聊',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '简单描述房间用途（可选）'
            })
        }
        labels = {
            'name': '房间名称',
            'description': '房间描述'
        }

    def clean_name(self):
        """校验房间名称：去重+长度"""
        name = self.cleaned_data.get('name').strip()
        if len(name) < 2:
            raise forms.ValidationError("房间名称至少2个字符！")
        if ChatRoom.objects.filter(name=name).exists():
            raise forms.ValidationError("该房间名称已存在！")
        return name


class ChatMessageForm(forms.ModelForm):
    """发送消息表单（优化：仅保留内容+样式）"""

    class Meta:
        model = ChatMessage
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '输入消息并回车发送...',
                'autocomplete': 'off',
                'required': True
            })
        }
        labels = {'content': ''}

    def clean_content(self):
        """校验消息内容：非空+去空格"""
        content = self.cleaned_data.get('content').strip()
        if not content:
            raise forms.ValidationError("消息内容不能为空！")
        return content