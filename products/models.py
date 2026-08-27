from django.utils import timezone
from django.db import models
from django.conf import settings


class category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    slug = models.SlugField(blank=True)
    stock = models.IntegerField(default=1)
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=0)
    product_image = models.ImageField(upload_to='photos/products', blank=True)
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        help_text='The account that listed this product.',
    )

    def __str__(self):
        return self.name