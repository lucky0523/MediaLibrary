from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone


class Movie(models.Model):
    imdb_id = models.CharField(max_length=32)
    douban_id = models.CharField(max_length=32)
    tmdb_id = models.CharField(max_length=32)
    title = models.CharField(max_length=200, default="", null=True, blank=True)
    douban_read = models.BooleanField(default=False)
    local_read = models.BooleanField(default=False)
    director = models.CharField(max_length=32, default="", null=True, blank=True)
    actor = models.CharField(max_length=32, default="", null=True, blank=True)
    year = models.IntegerField(default=0)
    path = models.CharField(max_length=32, default="", null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    file_size = models.FloatField(default=0)
    subtitle = models.CharField(max_length=32, default="", null=True, blank=True)
    resolution_enum = (
        (1, '2K'),
        (2, '4K')
    )
    resolution = models.SmallIntegerField(choices=resolution_enum, default=0)
    media_type_enum = (
        (1, 'Bluray'),
        (2, 'Remux'),
        (3, 'Web')
    )
    media_type = models.SmallIntegerField(choices=media_type_enum, default=0)
