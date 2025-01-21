from django.db import models
from django.utils.timezone import now
from datetime import timedelta

def default_expiry():
    return now() + timedelta(hours=24)

class URL(models.Model):
    original_url = models.URLField()
    short_url = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_expiry)

    def __str__(self):
        return self.short_url

class Analytics(models.Model):
    short_url = models.ForeignKey(URL, on_delete=models.CASCADE, related_name='analytics')
    access_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.short_url.short_url} accessed at {self.access_time}"
