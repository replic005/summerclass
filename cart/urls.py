from django.urls import path

from . import views

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('add-cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('decrement/<int:product_id>/', views.cart_decrement, name='cart_decrement'),
    path('remove-cart-item/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
]
