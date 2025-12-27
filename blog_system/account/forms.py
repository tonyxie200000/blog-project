from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, UserProfile

# 注册表单
class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': '请输入邮箱',
            'class': 'form-input'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': '请输入用户名',
                'class': 'form-input'
            }),
            'password1': forms.PasswordInput(attrs={
                'placeholder': '设置密码',
                'class': 'form-input'
            }),
            'password2': forms.PasswordInput(attrs={
                'placeholder': '确认密码',
                'class': 'form-input'
            })
        }

# 登录表单
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': '用户名',
            'class': 'form-input'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '密码',
            'class': 'form-input'
        })
    )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["nickname", "avatar", "bio"]  # 对应模型字段
