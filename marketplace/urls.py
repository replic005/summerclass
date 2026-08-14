"""
URL configuration for marketplace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('products/', include('products.urls')),
    path('blog/', include('blog.urls')),

    # --- accounts: managed directly here, no separate accounts app ---
    path('accounts/login/', views.user_login, name='user_login'),
    path('accounts/register/', views.user_register, name='user_register'),
    path('accounts/logout/', views.user_logout, name='user_logout'),

    path('accounts/activate/<uidb64>/<token>/', views.account_activate, name="account_activate"),

    path('accounts/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('accounts/edit-profile/', views.edit_profile, name='edit_profile'),
    path("accounts/my-products/", views.my_products, name="my_products"),
    path("accounts/product/<int:product_id>/edit/", views.edit_product, name="edit_product"),
    # path("accounts/product/<int:product_id>/delete/", views.delete_product, name="delete_product"),
    path("accounts/add-product/", views.add_product, name="add_product"),

    path('accounts/my-orders/', views.my_orders, name='my_orders'),
    path('accounts/order-detail/<int:order_id>/', views.order_detail, name="order_detail"),
    path('accounts/my-sales/', views.my_sales, name='my_sales'),
    path('accounts/my-sales/<int:order_product_id>/status/', views.update_delivery_status, name='seller_update_delivery_status'),

    path('accounts/forgot-password/', views.forgot_password, name='forgot_password'),
    path('accounts/forgot-password-validate/<uidb64>/<token>/', views.forgot_password_validate, name='forgot_password_validate'),

    path('accounts/reset-password/', views.reset_password, name='reset_password'),

    path('accounts/change-password/', views.change_password, name='change_password'),
    path('accounts/my-requests-sent/', views.my_requests_sent, name='my_requests_sent'),
    path("accounts/my-requests-received/", views.my_requests_received, name="my_requests_received"),
    path("accounts/fulfill/<int:pk>/", views.mark_request_fulfilled, name="mark_request_fulfilled"),
    path("accounts/reopen/<int:pk>/", views.reopen_request, name="reopen_request"),
]