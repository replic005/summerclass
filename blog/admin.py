from django.contrib import admin
from .models import blog

class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'published_date')

admin.site.register(blog, BlogAdmin)


