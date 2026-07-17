from django.shortcuts import render, get_object_or_404
from .models import product,category

def products(request):
    all_products = product.objects.all()
    return render(request, 'basic/products.html', {'products': all_products})

def product_detail(request,id):
    get_product = get_object_or_404(product, id=id)
    return render(request, 'basic/products/details.html', {'get_product': get_product})
