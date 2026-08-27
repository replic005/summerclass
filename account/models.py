import random
import string

from django.conf import settings
from django.db import models
from django.utils import timezone

from products.models import product as Product


# =========================
# PROFILE
# =========================

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    phone_number = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True, default='Nepal')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to='photos/profiles', blank=True, null=True
    )
    payment_qr = models.ImageField(
        upload_to='photos/payment_qr', blank=True, null=True,
        help_text='QR code buyers can scan to pay this seller directly.',
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.get_username()


# =========================
# ORDERS
# =========================

def _generate_order_number():
    stamp = timezone.now().strftime('%Y%m%d')
    suffix = ''.join(random.choices(string.digits, k=4))
    return f'{stamp}{suffix}'


class Order(models.Model):
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
    )
    order_number = models.CharField(max_length=20, unique=True, editable=False)

    # Billing / shipping snapshot taken at checkout time.
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100)
    order_note = models.TextField(blank=True)

    payment_method = models.CharField(max_length=50, default='Cash on Delivery')
    subtotal = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            number = _generate_order_number()
            while Order.objects.filter(order_number=number).exists():
                number = _generate_order_number()
            self.order_number = number
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()


class OrderItem(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_SHIPPED = 'shipped'
    STATUS_DELIVERED = 'delivered'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_SHIPPED, 'Shipped'),
        (STATUS_DELIVERED, 'Delivered'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, related_name='order_items'
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sales',
    )

    # Snapshot of product details so this stays accurate even if the
    # product is later edited, deleted, or its price changes.
    product_name = models.CharField(max_length=200)
    price = models.FloatField()
    quantity = models.PositiveIntegerField(default=1)

    delivery_status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quantity} x {self.product_name} ({self.order.order_number})'

    @property
    def item_total(self):
        return round(self.price * self.quantity, 2)


# =========================
# MESSAGES (buyer <-> seller communication)
# =========================

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='messages',
    )
    subject = models.CharField(max_length=200)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.subject} ({self.sender} -> {self.recipient})'


class MessageReply(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='replies')
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='message_replies',
    )
    body = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Reply by {self.sender} on {self.message_id}'
