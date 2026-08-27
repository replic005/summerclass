from django.contrib import admin

from .models import Message, MessageReply, Order, OrderItem, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'city', 'country', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone_number')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'price', 'quantity', 'seller')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'buyer', 'grand_total', 'created_at')
    search_fields = ('order_number', 'buyer__username', 'email')
    list_filter = ('created_at',)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'seller', 'quantity', 'delivery_status')
    list_filter = ('delivery_status',)
    search_fields = ('product_name', 'order__order_number', 'seller__username')


class MessageReplyInline(admin.TabularInline):
    model = MessageReply
    extra = 0


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'recipient', 'product', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('subject', 'sender__username', 'recipient__username')
    inlines = [MessageReplyInline]
