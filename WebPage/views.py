import json

from django.http import HttpResponse
from django.shortcuts import render

from MediaModel.models import Media
from MediaLibrary.common import Static


def imgs(request):
    # img_list = models.Img.objects.all()
    image_list = []
    mlist = Media.objects.all()
    for media in mlist:
        image_list.append(Static.PATH_FILMS_IMAGES[1:] + media.imdb_id + '/poster.jpg')
        pass
    context = {}
    context['Items'] = image_list
    return render(request, 'image.html', context)
