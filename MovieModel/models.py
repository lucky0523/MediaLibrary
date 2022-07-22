from django.db import models

# Create your models here.
from django.db import models


class Movie(models.Model):
    imdb_id = models.CharField(max_length=32)
    douban_id = models.CharField(max_length=32)
    tmdb_id = models.CharField(max_length=32)
    title = models.CharField(max_length=200,default="", null=True, blank=True)
    director = models.CharField(max_length=32,default="", null=True, blank=True)
