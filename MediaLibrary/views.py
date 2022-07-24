from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
    context = {}
    context['hello'] = 'Hello World!'
    context['name']='xxxx'
    context['pic']='/static/films_folder/tt2379713/post.webp'
    return render(request, 'demo.html', context)
