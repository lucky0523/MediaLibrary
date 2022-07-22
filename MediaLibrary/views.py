from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
    context = {}
    context['hello'] = 'Hello World!'
    context['name']='xxxx'
    return render(request, 'demo.html', context)
