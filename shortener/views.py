from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.utils.timezone import now
from .models import URL, Analytics
from .utils import generate_short_url
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from datetime import timedelta
from .models import URL
from .utils import generate_short_url

@csrf_exempt
def shorten_url(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        expiration_hours = request.POST.get('expiration_hours', 24)

        if not original_url:
            return JsonResponse({'error': 'Original URL is required'}, status=400)

        validator = URLValidator()
        try:
            validator(original_url)
        except ValidationError:
            return JsonResponse({'error': 'Invalid URL format'}, status=400)

        try:
            expiration_hours = int(expiration_hours)
        except ValueError:
            return JsonResponse({'error': 'Expiration hours must be an integer'}, status=400)

        short_url = generate_short_url(original_url)
        expires_at = now() + timedelta(hours=expiration_hours)

        url, created = URL.objects.get_or_create(
            original_url=original_url,
            defaults={'short_url': short_url, 'expires_at': expires_at}
        )

        return JsonResponse({'short_url': request.build_absolute_uri('/') + url.short_url}, status=201)

    return JsonResponse({'error': 'POST request required'}, status=400)

def redirect_url(request, short_url):
    url = get_object_or_404(URL, short_url=short_url)

    if url.expires_at < now():
        return HttpResponse("This URL has expired.", status=410)

    ip_address = get_client_ip(request)
    Analytics.objects.create(short_url=url, ip_address=ip_address)

    return redirect(url.original_url)

def get_analytics(request, short_url):
    url = get_object_or_404(URL, short_url=short_url)
    analytics = url.analytics.all()

    data = [
        {'access_time': log.access_time, 'ip_address': log.ip_address}
        for log in analytics
    ]

    return JsonResponse({'short_url': url.short_url, 'analytics': data})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
