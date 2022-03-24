from django.db import models
# from urllib import request ??
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=200, unique=True)
    image_url = models.URLField(null=True)
    genres = models.CharField(max_length=100, null=True)
    release_date = models.CharField(max_length=20, null=True)
    actor = models.CharField(max_length=100)
    character = models.CharField(max_length=200)
    tagline = models.CharField(max_length=200, null=True)
    summary = models.TextField(null=True)

    def __str__(self):
        return self.title
