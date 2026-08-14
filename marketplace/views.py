from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from products.models import category, product
from blog.models import blog


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


# =========================
# LOGIN
# =========================

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


# =========================
# REGISTER
# =========================

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not username or not email or not password:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'accounts/register.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'accounts/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'accounts/register.html')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            'Registration successful. Please login.'
        )

        return redirect('user_login')

    return render(request, 'accounts/register.html')


# =========================
# LOGOUT
# =========================

def user_logout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='user_login')
def user_dashboard(request):
    return render(request, 'accounts/dashboard.html')


@login_required(login_url='user_login')
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if username:
            user.username = username

        if email:
            user.email = email

        user.first_name = first_name or ''
        user.last_name = last_name or ''

        user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('user_dashboard')

    return render(
        request,
        'accounts/edit_profile.html',
        {'user': user}
    )


# =========================
# MY PRODUCTS
# =========================

@login_required(login_url='user_login')
def my_products(request):
    # The product model has no user/seller field.
    # Therefore we cannot filter products by owner.
    products = product.objects.all()

    return render(
        request,
        'accounts/my_products.html',
        {'products': products}
    )


# =========================
# EDIT PRODUCT
# =========================

@login_required(login_url='user_login')
def edit_product(request, product_id):
    item = get_object_or_404(product, id=product_id)
    categories = category.objects.all()

    if request.method == 'POST':
        item.name = request.POST.get('name')
        item.description = request.POST.get('description')
        item.price = request.POST.get('price')
        item.stock = request.POST.get('stock')

        category_id = request.POST.get('category')

        if category_id:
            item.category_id = category_id

        if request.FILES.get('product_image'):
            item.product_image = request.FILES.get('product_image')

        item.save()

        messages.success(request, 'Product updated successfully.')
        return redirect('my_products')

    return render(
        request,
        'accounts/edit_product.html',
        {
            'product': item,
            'categories': categories,
        }
    )


# =========================
# ADD PRODUCT
# =========================

@login_required(login_url='user_login')
def add_product(request):
    categories = category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        category_id = request.POST.get('category')
        product_image = request.FILES.get('product_image')

        if not name or not price or not category_id:
            messages.error(
                request,
                'Please fill in all required fields.'
            )

            return render(
                request,
                'accounts/add_product.html',
                {'categories': categories}
            )

        product.objects.create(
            name=name,
            description=description,
            price=price,
            stock=stock or 1,
            category_id=category_id,
            product_image=product_image
        )

        messages.success(request, 'Product added successfully.')
        return redirect('my_products')

    return render(
        request,
        'accounts/add_product.html',
        {'categories': categories}
    )


# =========================
# MY ORDERS
# =========================

@login_required(login_url='user_login')
def my_orders(request):
    return render(
        request,
        'accounts/my_orders.html',
        {'orders': []}
    )


# =========================
# ORDER DETAIL
# =========================

@login_required(login_url='user_login')
def order_detail(request, order_id):
    return render(
        request,
        'accounts/order_detail.html',
        {'order_id': order_id}
    )


# =========================
# MY SALES
# =========================

@login_required(login_url='user_login')
def my_sales(request):
    return render(
        request,
        'accounts/my_sales.html',
        {'sales': []}
    )


# =========================
# UPDATE DELIVERY STATUS
# =========================

@login_required(login_url='user_login')
def update_delivery_status(request, order_product_id):
    if request.method == 'POST':
        messages.success(
            request,
            'Delivery status updated.'
        )

    return redirect('my_sales')


# =========================
# FORGOT PASSWORD
# =========================

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if User.objects.filter(email=email).exists():
            messages.success(
                request,
                'Password reset request received.'
            )
            return redirect('reset_password')

        messages.error(
            request,
            'No account was found with this email.'
        )

    return render(request, 'accounts/forgot_password.html')


# =========================
# RESET PASSWORD
# =========================

def reset_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(
                request,
                'accounts/reset_password.html'
            )

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return render(
                request,
                'accounts/reset_password.html'
            )

        user.set_password(password)
        user.save()

        messages.success(
            request,
            'Password reset successfully.'
        )

        return redirect('user_login')

    return render(request, 'accounts/reset_password.html')


# =========================
# CHANGE PASSWORD
# =========================

@login_required(login_url='user_login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():
            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            messages.success(
                request,
                'Password changed successfully.'
            )

            return redirect('user_dashboard')

    else:
        form = PasswordChangeForm(request.user)

    return render(
        request,
        'accounts/change_password.html',
        {'form': form}
    )