from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import  Category
from .forms import PostForm
# 在views.py顶部添加导入
from .models import Post, Comment  # 新增Comment

# 文章列表（首页）
def post_list(request):
    posts = Post.objects.filter(is_deleted=False, is_published=True).order_by('-created_at')
    return render(request, 'post/index.html', {'posts': posts})


# 文章详情
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, is_deleted=False)
    post.increase_views()
    return render(request, 'post/detail.html', {'post': post})


# 关于页面
def post_about(request):
    return render(request, 'post/about.html')


# 发布文章（需登录）
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, '文章发布成功！')
            return redirect('post:detail', pk=post.id)
    else:
        form = PostForm()
    return render(request, 'post/create.html', {'form': form})


# 编辑文章（仅作者可编辑）
@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user, is_deleted=False)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, '文章编辑成功！')
            return redirect('post:detail', pk=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'post/create.html', {'form': form, 'post': post})


# 删除文章（软删除）
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user, is_deleted=False)
    post.soft_delete()
    messages.success(request, '文章已删除！')
    return redirect('post:index')


# 评论（占位）
@login_required
def post_comment(request, pk):
    post = get_object_or_404(Post, pk=pk, is_deleted=False)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            messages.success(request, '评论提交成功！')
        else:
            messages.error(request, '评论内容不能为空！')
    return redirect('post:detail', pk=pk)


# 新增分类接口（AJAX调用，需登录+POST请求）
@login_required
@require_POST
def category_create(request):
    """AJAX新增分类的后端接口"""
    # 获取前端传的分类名称
    name = request.POST.get('name', '').strip()

    # 校验分类名称非空
    if not name:
        return JsonResponse({'code': 400, 'msg': '分类名称不能为空'})

    # 校验分类是否已存在（未删除的同名分类）
    if Category.objects.filter(name=name, is_deleted=False).exists():
        return JsonResponse({'code': 400, 'msg': '该分类已存在'})

    # 创建分类（关联当前登录用户为创建人）
    category = Category.objects.create(
        name=name,
        creator=request.user
    )

    # 返回成功结果（包含分类ID和名称，供前端更新下拉框）
    return JsonResponse({
        'code': 200,
        'msg': '分类创建成功',
        'data': {'id': category.id, 'name': category.name}
    })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, is_deleted=False)
    post.increase_views()
    # 获取该文章的所有评论
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    return render(request, 'post/detail.html', {
        'post': post,
        'comments': comments
    })

@login_required
def post_comment(request, pk):
    post = get_object_or_404(Post, pk=pk, is_deleted=False)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )
            messages.success(request, '评论提交成功！')
        else:
            messages.error(request, '评论内容不能为空！')
    return redirect('post:detail', pk=pk)