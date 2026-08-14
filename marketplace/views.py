from django.shortcuts import render
from django.http import HttpResponse
from products.models import category, product
from blog.models import blog

def home(request):
    products = product.objects.all().filter(status=True)
    categories = category.objects.all().filter(status=True)
    blogs = blog.objects.all().filter(status=True)

    context = {
        'products': products,
        'categories': categories,
        'blogs': blogs,
    }

    return render(request, 'new_design/home.html', context)
