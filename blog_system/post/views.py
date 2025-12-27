from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import  Category, Post
from .forms import PostForm,PostPublishForm
# 在views.py顶部添加导入
from .models import Post, Comment  # 新增Comment

# 按分类筛选文章（复用你现有的Category模型）
def post_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category)  # 你的文章已关联category
    return render(request, "post/index.html", {"posts": posts, "current_category": category})


# 文章列表（首页）
def post_list(request):

    posts = Post.objects.all().order_by('-created_at')

    categories = Category.objects.all()  # 新增：获取所有分类
    return render(request, 'post/index.html', {
        'posts': posts,
        "page_type": "all",  # 模板需要的page_type
        'categories': categories  # 传递给模板
    })


# 文章详情
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, is_published=Ture)
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
            return redirect('post:post_detail', pk=post.id)
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
            return redirect('post:post_detail', pk=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'post/create.html', {'form': form, 'post': post})


@login_required
def post_edit(request, pk):
    # 获取文章，且仅允许作者编辑
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "文章编辑成功！")
            return redirect("post:post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, "post/post_form.html", {"form": form, "title": "编辑文章"})


# 文章删除视图（仅作者可操作）
@login_required
def post_delete(request, pk):
    # 获取文章，且仅允许作者删除
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == "POST":
        post.delete()
        messages.success(request, "文章删除成功！")
        return redirect("post:index")  # 删完跳转到文章列表页
    # GET请求显示确认页面
    return render(request, "post/post_confirm_delete.html", {"post": post})


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
    return redirect('post:post_detail', pk=pk)

@login_required
def my_posts(request):
    # 获取当前用户发布的文章
    user_posts = Post.objects.filter(author=request.user)
    return render(request, "post/my_posts.html", {"posts": user_posts})

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
    post = get_object_or_404(Post, pk=pk, is_published=True)
    post.increase_views()
    # 获取该文章的所有评论
    comments = Comment.objects.filter(post=post).order_by('-created_at')
    return render(request, 'post/detail.html', {
        'post': post,
        
        'comments': comments,
    })

@login_required
def post_comment(request, pk):
    post = get_object_or_404(Post, pk=pk, is_published=True)
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
    return redirect('post:post_detail', pk=pk)


@login_required(login_url="/admin/login/")  # 未登录则跳转到登录页
def post_publish(request):
    if request.method == "POST":
        # 提交表单时
        form = PostPublishForm(request.POST)
        if form.is_valid():
            # 先保存表单（不提交到数据库）
            post = form.save(commit=False)
            # 自动填充作者（当前登录用户）
            post.author = request.user
            # 自动设置为发布状态
            post.is_published = True
            # 提交到数据库
            post.save()
            # 提示发布成功
            messages.success(request, "文章发布成功！")
            # 跳转到文章详情页/首页
            return redirect("post:post_detail", pk=post.pk)  # 需确保有post_detail路由
    else:
        # GET请求：显示空表单
        form = PostPublishForm()

    # 渲染发布页面
    return render(
        request,
        "post/publish.html",  # 对应发布页面模板
        {"form": form, "title": "发布新文章"}
    )
