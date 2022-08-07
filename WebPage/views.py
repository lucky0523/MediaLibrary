import json

from django.http import HttpResponse
from django.shortcuts import render

from MediaModel.models import Media
from MediaLibrary.common import Static


def imgs(request):
    # img_list = models.Img.objects.all()
    view_list = []
    mlist = Media.objects.all()
    for media in mlist:
        view_dict = {}
        view_dict['year'] = media.release_date.year
        view_dict['disk']=media.disk_sn
        view_dict['path']=media.path
        try:
            view_dict['title'] = eval(media.i18n_title)[Static.LANGUAGE]
            view_dict['image'] = eval(media.image_paths)[Static.KEY_IMAGE_CATEGORY_POSTER][1:]
            print(view_dict['image'])
        except SyntaxError as e:
            print(e)
            view_dict['title'] = '标题错误'
            view_dict['image'] = ''
        print(view_dict)
        view_list.append(view_dict)
        pass
    context = {}
    context['Items'] = view_list
    return render(request, 'image.html', context)
