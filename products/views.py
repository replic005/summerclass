from django.shortcuts import render, get_object_or_404
from .models import product, category

def products(request):
    products = product.objects.all()
    return render(
        request,
        'templates copy/products/products.html',
        {'products': products}
    )

def product_detail(request, id):
    get_product = get_object_or_404(product, id=id)
    return render(
        request,
        'templates copy/products/details.html',
        {'get_product': get_product}
    )