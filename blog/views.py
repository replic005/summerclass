from django.shortcuts import render,get_object_or_404
from .models import blog

# blog/views.py
def blog_list(request):
    blogs = blog.objects.all()
    return render(request, 'extending/blogs.html', {'blogs': blogs})

def blog_detail(request, id):
    blog_post = get_object_or_404(blog, id=id)
    return render(request, 'extending/blog_details.html', {'blog_post': blog_post})
