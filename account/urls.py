from django.urls import path

from . import views

urlpatterns = [
    # --- auth ---
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
    path('logout/', views.user_logout, name='user_logout'),

    # --- dashboard / profile ---
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    # --- products (seller) ---
    path('my-products/', views.my_products, name='my_products'),
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('add-product/', views.add_product, name='add_product'),

    # --- orders (buyer) ---
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order-detail/<int:order_id>/', views.order_detail, name='order_detail'),

    # --- sales (seller) ---
    path('my-sales/', views.my_sales, name='my_sales'),
    path(
        'my-sales/<int:order_product_id>/status/',
        views.update_delivery_status,
        name='seller_update_delivery_status',
    ),

    # --- public seller storefront ---
    path('seller/<int:seller_id>/', views.seller_profile, name='seller_profile'),

    # --- messages ---
    path('messages/inbox/', views.messages_inbox, name='messages_inbox'),
    path('messages/sent/', views.messages_sent, name='messages_sent'),
    path('messages/<int:message_id>/', views.message_detail, name='message_detail'),
    path('messages/<int:message_id>/reply/', views.message_reply, name='message_reply'),
    path('message/new/<int:product_id>/', views.contact_seller, name='contact_seller'),

    # --- password ---
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('change-password/', views.change_password, name='change_password'),
]
