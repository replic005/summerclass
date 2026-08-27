from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from .models import product, category


def products(request):
    items = product.objects.filter(status=True)
    categories = category.objects.all()

    keyword = request.GET.get('keyword', '').strip()
    selected_category = request.GET.get('category', '').strip()

    if keyword:
        items = items.filter(
            Q(name__icontains=keyword) | Q(description__icontains=keyword)
        )

    if selected_category:
        items = items.filter(category_id=selected_category)

    context = {
        'products': items,
        'categories': categories,
        'keyword': keyword,
        'selected_category': selected_category,
    }
    return render(request, 'products/products.html', context)


def product_detail(request, id):
    get_product = get_object_or_404(product, id=id)
    return render(request, 'products/details.html', {'get_product': get_product})
