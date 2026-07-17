from django.urls import path
from . import views

urlpattherns = [
    path('<slug:slug>/', views.page_detail, name='page_detail'),
]