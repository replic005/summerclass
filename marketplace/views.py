from django.shortcuts import render
from django.http import HttpResponse
from products.models import category, product
from blog.models import blog

def home(request):
    products = product.objects.all()
    blogs = blog.objects.all().order_by('-published_date')
    
    return render(request, 'templates copy/home/home1.html', {
        'products': products,
        'blogs': blogs,
    })
