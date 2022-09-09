from django.shortcuts import render
from .models import Blog

def all_blogs(request):
    # Но тут лучше бы использовать пагинатор
    blogs = Blog.objects.order_by('-created')[:5]
    return render(request, 'blog/all_blogs.html', {'blogs': blogs})
