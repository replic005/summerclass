from . models import SiteSetting


def site_settings(request):
    site_settings = SiteSetting.objects.first()
    return {'site_settings': site_settings}