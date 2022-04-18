from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from .models import Group, Post, User
from .forms import PostForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()


def paginator(request, collection):
    paginator = Paginator(collection, 10)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    posts = Post.objects.order_by('-pub_date')
    page_obj = paginator(request, posts)
    template = 'posts/index.html'
    context = {
        'page_obj': page_obj,
        'posts': page_obj.object_list
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    page_obj = paginator(request, posts)
    context = {
        'group': group,
        'posts': posts,
        'page_obj': page_obj
    }
    return render(request, template, context)



# def group_posts(request, slug):
#     group = get_object_or_404(Group, slug=slug)
#     posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
#     context = {
#         'group': group,
#         'posts': posts,
#     }
#     return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    page_obj = paginator(request, posts)
    post_kol = posts.count()
    context = {
        'author': author,
        'posts': posts,
        'page_obj': page_obj,
        'post_count': post_kol,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author = post.author
    author_posts = author.posts
    post_count = author_posts.count()
    context = {
        'author': author,
        'title': post.text,
        'post': post,
        'post_count': post_count,
    }
    return render(request, 'posts/post_detail.html', context)

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', username=post.author)

        return render(request, 'posts/create_post.html', {'form': form})

    form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    is_edit = True
    form = PostForm(request.POST or None, instance=post)
    if post.author == request.user:
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post.text = form.cleaned_data['text']
                post.group = form.cleaned_data['group']
                post.save()
                return redirect('posts:post_detail', post.pk)
        form = PostForm(request.POST or None, instance=post)
        return render(request, 'posts/create_post.html', {'form': form, 'is_edit': is_edit, 'post_id': post.pk})
    return render(request, 'posts/create_post.html', {'form': form, 'is_edit': False})
