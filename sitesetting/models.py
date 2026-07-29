from django.db import models

class SiteSetting(models.Model):
    site_title = models.CharField(max_length=200, default='Marketplace')
    site_description = models.TextField(blank=True,null=True)
    site_keywords = models.CharField(max_length=225, blank=True,null=True)
    logo = models.ImageField(upload_to="photos/logo/", blank=True, null=True)
    favicon = models.ImageField(upload_to="photos/favicon/", blank=True, null=True)

    def __str__(self):
        return "Site Setting"
    
    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"
