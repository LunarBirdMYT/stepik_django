from django.shortcuts import get_object_or_404, render
from .models import Blog

def all_blogs(request):
    # Но тут лучше бы использовать пагинатор
    blogs = Blog.objects.order_by('-created')
    return render(request, 'blog/all_blogs.html', {'blogs': blogs})

def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'blog/detail.html', {'blog': blog})
