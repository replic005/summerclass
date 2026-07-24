from django.db import models

# Create your models here.
class blog (models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.CharField(max_length=100)
    published_date = models.DateTimeField(auto_now_add=True)
    blog_image = models.ImageField(upload_to='photos/blogs', blank=True)
    
    def __str__(self):
        return self.title