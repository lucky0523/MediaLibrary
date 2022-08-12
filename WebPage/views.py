import json

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from MediaModel.models import Media
from MediaLibrary.common import Static


def imgs(request):
    # img_list = models.Img.objects.all()
    one_page_count = 24
    page = 1
    try:
        page = int(request.GET.get('page', 1))
    except ValueError as e:
        print(e)
    view_list = []
    mlist = Media.objects.filter(~Q(imdb_id=''))
    mlist = mlist[one_page_count * (page - 1):one_page_count * page]
    for media in mlist:
        view_dict = {}
        view_dict['year'] = media.release_date.year
        view_dict['disk'] = media.disk_sn
        view_dict['path'] = media.path
        view_dict['title'] = media.get_i18n_title()
        try:
            view_dict['image'] = eval(media.image_paths)[Static.KEY_IMAGE_CATEGORY_POSTER][1:]
        except SyntaxError as e:
            print(e)
        if 'image' not in view_dict or view_dict['image'] == '':
            view_dict['image'] = '/static/images/no-image.png'
        view_list.append(view_dict)
        pass
    context = {}
    context['Items'] = view_list
    return render(request, 'image.html', context)
