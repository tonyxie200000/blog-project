from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegisterForm, LoginForm

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