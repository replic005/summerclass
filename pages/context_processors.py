from .models import Page

def pages_links(request):
    pages = Page.objects.all()
    return {
        'pages_links': pages
    }