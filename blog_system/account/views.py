from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from .models import User, Profile


def user_profile(request, username):
    # 根据用户名获取目标用户
    target_user = get_object_or_404(User, username=username)
    # 获取该用户的Profile（不存在则自动创建）
    profile, created = UserProfile.objects.get_or_create(user=target_user)
    # 传递数据到模板
    return render(request, "account/user_profile.html", {
        "profile": profile,
        "target_user": target_user
    })

# 登录
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, '登录成功！')
            return redirect('index')
        else:
            messages.error(request, '用户名或密码错误！')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

# 登出
def user_logout(request):
    logout(request)
    messages.success(request, '已成功登出！')
    return redirect('index')

# 注册
def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '注册并登录成功！')
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'account/register.html', {'form': form})

@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("account:profile")  # 跳转到个人资料页
    else:
        form = ProfileForm(instance=profile)
    return render(request, "account/profile_edit.html", {"form": form})

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, "account/profile.html", {"profile": request.user.profile})
