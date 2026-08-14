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
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    return redirect('home')