import json

from django.http import HttpResponse
from django.shortcuts import render


def imgs(request):
    # img_list = models.Img.objects.all()
    image_list = []
    image_list.append('/static/films_folder/tt0099785/post.webp')
    image_list.append('/static/films_folder/tt2379713/post.webp')
    context = {}
    context['Items'] = image_list
    return render(request, 'image.html', context)
