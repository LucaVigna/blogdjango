# blog/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from django import forms
from .models import Post, Category, Comment


def index(request):
    """Vista principal del blog"""
    posts = Post.objects.filter(status='published').select_related('category', 'author')
    categories = Category.objects.all()
    
    # Paginación
    paginator = Paginator(posts, 6)  # 6 posts por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'posts': page_obj,
        'categories': categories,
        'title': 'Blog'
    }
    return render(request, 'blog/index.html', context)


def post_detail(request, slug):
    """Vista de detalle de un post"""
    post = get_object_or_404(Post, slug=slug, status='published')
    comments = post.comments.filter(active=True)
    
    # Manejar formulario de comentarios
    if request.method == 'POST':
        author = request.POST.get('author')
        email = request.POST.get('email')
        content = request.POST.get('content')
        
        if author and email and content:
            Comment.objects.create(
                post=post,
                author=author,
                email=email,
                content=content
            )
            return redirect('blog:post_detail', slug=post.slug)
    
    # Posts relacionados (misma categoría)
    related_posts = Post.objects.filter(
        category=post.category, 
        status='published'
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'comments': comments,
        'related_posts': related_posts,
        'title': post.title
    }
    return render(request, 'blog/detail.html', context)  # 👈 Cambiado aquí


def category_posts(request, slug):
    """Vista de posts por categoría"""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published')
    
    # Paginación
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'posts': page_obj,
        'title': f'Categoría: {category.name}'
    }
    return render(request, 'blog/category.html', context)


# -------- NUEVO: Crear post solo para admin/staff -------- #

class PostForm(forms.ModelForm):
    """Formulario para crear posts"""
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'status', 'featured_image']


@staff_member_required   # 👈 Solo usuarios staff/admin pueden acceder
def post_create(request):
    """Vista para crear un post (solo admin/staff)"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # asigna el admin como autor
            post.save()
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm()
    
    return render(request, 'blog/post_form.html', {
        'form': form,
        'title': 'Nuevo Post'
    })