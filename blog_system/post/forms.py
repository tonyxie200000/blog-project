from django import forms
from .models import Post, Category


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'content', 'is_published')
        # 完善控件配置
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '文章标题'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 10,
                'placeholder': '文章内容'
            }),
            # 分类下拉框仅显示未删除的分类
            'category': forms.Select(attrs={'class': 'form-select'})
        }
        labels = {
            'title': '标题',
            'category': '分类',
            'content': '内容',
            'is_published': '是否发布'
        }

    # 重写category字段，仅显示未删除的分类
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()

class PostPublishForm(forms.ModelForm):
    """前台文章发布表单（简化版，适合普通用户）"""
    # 简化分类选择（只显示已有的分类）
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="选择分类（可选）",
        required=False,  # 分类可选
        widget=forms.Select(attrs={
            "class": "form-control",
            "placeholder": "选择文章分类"
        })
    )

    class Meta:
        model = Post  # 关联Post模型
        fields = ["title", "content", "category"]  # 只显示普通用户需要的字段
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "输入文章标题（不超过200字）",
                "maxlength": 200
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "输入文章内容",
                "rows": 10,  # 文本框高度
                "style": "resize: vertical;"  # 允许垂直拉伸
            })
        }
        labels = {
            "title": "文章标题",
            "content": "文章内容",
            "category": "文章分类"
        }
