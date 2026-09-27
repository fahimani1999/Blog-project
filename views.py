from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render, get_object_or_404

from .form import BlogPostForm
from .models import BlogPost


def home(request):
    posts = BlogPost.objects.select_related('author').order_by('-created_at')
    return render(request, 'home.html', {'posts': posts, 'page_title': 'Latest Blog Posts'})


def post_detail(request, id):

    post = get_object_or_404(
        BlogPost,
        id=id
    )

    return render(
        request,
        'post_detail.html',
        {
            'post': post
        }
    )


@login_required
def create_post(request):
    form = BlogPostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('post_detail', id=post.id)
    return render(request, 'post_form.html', {'form': form, 'page_title': 'Create Post'})


@login_required
def edit_post(request, id):
    post = get_object_or_404(BlogPost, id=id, author=request.user)
    form = BlogPostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('post_detail', id=post.id)
    return render(request, 'post_form.html', {'form': form, 'page_title': 'Edit Post'})


@login_required
def delete_post(request, id):
    post = get_object_or_404(BlogPost, id=id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'post_confirm_delete.html', {'post': post})


def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')
    return render(request, 'register.html', {'form': form})


def login_view(request):
    error = None
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if user is not None:
            login(request, user)
            return redirect('home')
        error = 'Invalid username or password.'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def my_posts(request):
    posts = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'home.html', {'posts': posts, 'page_title': 'My Posts'})