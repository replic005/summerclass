from django.db import models
from django.shortcuts import render

from products.models import category, product
from blog.models import blog


# =========================
# SEARCH
# =========================

def product_search(request):
    keyword = request.GET.get('keyword', '').strip()

    results = product.objects.filter(status=True)
    if keyword:
        results = results.filter(
            models.Q(name__icontains=keyword) |
            models.Q(description__icontains=keyword)
        )

    categories = category.objects.all()

    context = {
        'products': results,
        'categories': categories,
        'keyword': keyword,
        'selected_category': '',
    }
    return render(request, 'products/products.html', context)


# =========================
# HOME
# =========================

def home(request):
    products = product.objects.filter(status=True)
    categories = category.objects.all()
    blogs = blog.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'blogs': blogs,
    }

    return render(request, 'new_design/home.html', context)
