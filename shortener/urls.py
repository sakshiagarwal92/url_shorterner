from django.urls import path
from .views import shorten_url, redirect_url, get_analytics

urlpatterns = [
    path('shorten/', shorten_url, name='shorten'),
    path('<str:short_url>/', redirect_url, name='redirect'),
    path('analytics/<str:short_url>/', get_analytics, name='analytics'),
]
