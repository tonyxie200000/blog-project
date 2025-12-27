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
        self.fields['category'].queryset = Category.objects.filter(is_deleted=False)