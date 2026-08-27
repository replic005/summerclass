from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from products.models import product as Product

from .models import CartItem

TAX_RATE = 0.02


def _cart_totals(cart_items):
    subtotal = sum(item.item_total for item in cart_items)
    tax = round(subtotal * TAX_RATE, 2)
    grand_total = round(subtotal + tax, 2)
    return subtotal, tax, grand_total


@login_required(login_url='user_login')
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    subtotal, tax, grand_total = _cart_totals(cart_items)

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'account/cart.html', context)


@login_required(login_url='user_login')
def add_cart(request, product_id):
    item = get_object_or_404(Product, id=product_id)

    if item.stock < 1:
        messages.error(request, 'This product is out of stock.')
        return redirect('cart')

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=item,
        defaults={'quantity': 1},
    )

    if not created:
        if cart_item.quantity < item.stock:
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.error(request, 'No more stock available for this item.')
    else:
        messages.success(request, f'{item.name} added to your cart.')

    return redirect('cart')


@login_required(login_url='user_login')
def cart_decrement(request, product_id):
    cart_item = get_object_or_404(CartItem, user=request.user, product_id=product_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


@login_required(login_url='user_login')
def remove_cart_item(request, product_id):
    CartItem.objects.filter(user=request.user, product_id=product_id).delete()
    messages.success(request, 'Item removed from your cart.')
    return redirect('cart')


@login_required(login_url='user_login')
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')

    if not cart_items:
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')

    subtotal, tax, grand_total = _cart_totals(cart_items)

    if request.method == 'POST':
        # No real payment processing is wired up yet; this simply clears
        # the cart and confirms the (mock) order was placed.
        cart_items.delete()
        messages.success(request, 'Your order has been placed successfully.')
        return redirect('my_orders')

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'account/checkout.html', context)
