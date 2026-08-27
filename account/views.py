from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from products.models import category, product

from .forms import (
    ChangePasswordForm, MessageForm, MessageReplyForm, ProductForm,
    ProfileForm, RegisterForm,
)
from .models import Message, Order, OrderItem, Profile


# =========================
# LOGIN / REGISTER / LOGOUT
# =========================

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        username = None
        existing = User.objects.filter(email=email).first()
        if existing is not None:
            username = existing.username

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next')
            return redirect(next_url or 'home')

        messages.error(request, 'Invalid email or password.')

    return render(request, 'new_design/signin.html')


def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if not form.is_valid():
            for error_list in form.errors.values():
                for error in error_list:
                    messages.error(request, error)
            return render(request, 'new_design/register.html')

        data = form.cleaned_data

        # The site logs in with email, but Django's User model needs a
        # username. Use the email as the username since it's unique.
        user = User.objects.create_user(
            username=data['email'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data.get('last_name') or '',
        )

        profile, _ = Profile.objects.get_or_create(user=user)
        profile.phone_number = data.get('phone_number') or ''
        profile.save()

        messages.success(request, 'Registration successful. Please login.')
        return redirect('user_login')

    return render(request, 'new_design/register.html')


def user_logout(request):
    logout(request)
    return redirect('home')


# =========================
# DASHBOARD
# =========================

@login_required(login_url='user_login')
def user_dashboard(request):
    my_products_qs = product.objects.filter(seller=request.user)
    my_orders_qs = Order.objects.filter(buyer=request.user)
    my_sales_qs = OrderItem.objects.filter(seller=request.user)

    context = {
        'products_count': my_products_qs.count(),
        'active_products_count': my_products_qs.filter(status=True).count(),
        'inactive_products_count': my_products_qs.filter(status=False).count(),
        'orders_count': my_orders_qs.count(),
        'sales_count': my_sales_qs.count(),
    }
    context['active'] = 'dashboard'
    return render(request, 'account/dashboard.html', context)


# =========================
# PROFILE
# =========================

@login_required(login_url='user_login')
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('user_dashboard')

        for error_list in form.errors.values():
            for error in error_list:
                messages.error(request, error)

    return render(request, 'account/profile.html', {'profile': profile, 'active': 'profile'})


# =========================
# MY PRODUCTS (seller)
# =========================

@login_required(login_url='user_login')
def my_products(request):
    products = product.objects.filter(seller=request.user).order_by('-created_at')

    context = {
        'products': products,
        'total_count': products.count(),
        'active_count': products.filter(status=True).count(),
        'inactive_count': products.filter(status=False).count(),
    }
    context['active'] = 'myproducts'
    return render(request, 'account/myproducts.html', context)


@login_required(login_url='user_login')
def add_product(request):
    categories = category.objects.all()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.seller = request.user
            new_product.save()
            messages.success(request, 'Product added successfully.')
            return redirect('my_products')

        for error_list in form.errors.values():
            for error in error_list:
                messages.error(request, error)

    return render(request, 'account/addproducts.html', {'categories': categories, 'active': 'addproduct'})


@login_required(login_url='user_login')
def edit_product(request, product_id):
    item = get_object_or_404(product, id=product_id, seller=request.user)
    categories = category.objects.all()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('my_products')

        for error_list in form.errors.values():
            for error in error_list:
                messages.error(request, error)

    return render(
        request, 'account/addproducts.html',
        {'product': item, 'categories': categories, 'active': 'addproduct'},
    )


# =========================
# MY ORDERS (buyer)
# =========================

@login_required(login_url='user_login')
def my_orders(request):
    orders = Order.objects.filter(buyer=request.user).prefetch_related('items')
    return render(request, 'account/my-orders.html', {'orders': orders, 'active': 'myorders'})


@login_required(login_url='user_login')
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    return render(request, 'account/placeorder.html', {'order': order, 'active': 'myorders'})


# =========================
# MY SALES (seller)
# =========================

@login_required(login_url='user_login')
def my_sales(request):
    sale_items = OrderItem.objects.filter(seller=request.user).select_related('order', 'product')
    return render(request, 'account/mysales.html', {'sale_items': sale_items, 'active': 'mysales'})


@login_required(login_url='user_login')
def update_delivery_status(request, order_product_id):
    item = get_object_or_404(OrderItem, id=order_product_id, seller=request.user)

    if request.method == 'POST':
        status = request.POST.get('delivery_status')
        valid_statuses = dict(OrderItem.STATUS_CHOICES)
        if status in valid_statuses:
            item.delivery_status = status
            item.save()
            messages.success(request, 'Delivery status updated.')
        else:
            messages.error(request, 'Invalid delivery status.')

    return redirect('my_sales')


# =========================
# PUBLIC SELLER PROFILE
# =========================

def seller_profile(request, seller_id):
    seller = get_object_or_404(User, id=seller_id)
    seller_products = product.objects.filter(seller=seller, status=True)
    profile, _ = Profile.objects.get_or_create(user=seller)

    context = {
        'seller': seller,
        'profile': profile,
        'seller_products': seller_products,
    }
    return render(request, 'account/selllerprofile.html', context)


# =========================
# MESSAGES (buyer <-> seller)
# =========================

@login_required(login_url='user_login')
def messages_inbox(request):
    thread_list = Message.objects.filter(recipient=request.user)
    return render(
        request, 'account/messages.html',
        {'message_list': thread_list, 'box': 'inbox', 'active': 'inbox'},
    )


@login_required(login_url='user_login')
def messages_sent(request):
    thread_list = Message.objects.filter(sender=request.user)
    return render(
        request, 'account/messages.html',
        {'message_list': thread_list, 'box': 'sent', 'active': 'sent'},
    )


@login_required(login_url='user_login')
def message_detail(request, message_id):
    thread = get_object_or_404(
        Message.objects.filter(Q(sender=request.user) | Q(recipient=request.user)),
        id=message_id,
    )

    if thread.recipient == request.user and not thread.is_read:
        thread.is_read = True
        thread.save(update_fields=['is_read'])

    return render(request, 'account/message.html', {'thread': thread, 'active': 'inbox'})


@login_required(login_url='user_login')
def message_reply(request, message_id):
    thread = get_object_or_404(
        Message.objects.filter(Q(sender=request.user) | Q(recipient=request.user)),
        id=message_id,
    )

    if request.method == 'POST':
        form = MessageReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.message = thread
            reply.sender = request.user
            reply.save()
            messages.success(request, 'Reply sent.')
        else:
            messages.error(request, 'Please write a reply before sending.')

    return redirect('message_detail', message_id=thread.id)


@login_required(login_url='user_login')
def contact_seller(request, product_id):
    item = get_object_or_404(product, id=product_id)

    if item.seller_id is None:
        messages.error(request, 'This product has no seller to contact.')
        return redirect('product_detail', id=product_id)

    if item.seller_id == request.user.id:
        messages.error(request, "You can't message yourself about your own product.")
        return redirect('product_detail', id=product_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.sender = request.user
            new_message.recipient = item.seller
            new_message.product = item
            new_message.save()
            messages.success(request, 'Message sent to the seller.')
            return redirect('messages_sent')
        for error_list in form.errors.values():
            for error in error_list:
                messages.error(request, error)
    else:
        form = MessageForm(initial={'subject': f'About: {item.name}'})

    return render(
        request, 'account/message_new.html',
        {'form': form, 'product': item},
    )


# =========================
# FORGOT / RESET / CHANGE PASSWORD
# =========================

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if User.objects.filter(email=email).exists():
            messages.success(request, 'Password reset request received.')
            return redirect('reset_password')

        messages.error(request, 'No account was found with this email.')

    return render(request, 'account/forgot_password.html')


def reset_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'account/reset_password.html')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return render(request, 'account/reset_password.html')

        user.set_password(password)
        user.save()

        messages.success(request, 'Password reset successfully.')
        return redirect('user_login')

    return render(request, 'account/reset_password.html')


@login_required(login_url='user_login')
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)

        if form.is_valid():
            request.user.set_password(form.cleaned_data['new_password'])
            request.user.save()
            messages.success(request, 'Password changed successfully. Please login again.')
            return redirect('user_login')

        for error_list in form.errors.values():
            for error in error_list:
                messages.error(request, error)

    return render(request, 'account/password.html', {'active': 'password'})
