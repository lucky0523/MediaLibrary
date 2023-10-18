import json
import logging

from django.db import connection
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from MediaModel.models import Media
from HardDiskModel.models import HardDisk
from MediaLibrary.common import Static

LOG_TAG = '[WebPage.views] '
logging.basicConfig(level=Static.LOG_LEVEL, format='%(asctime)s - %(name)s %(levelname)s - %(message)s')
logger = logging.getLogger(LOG_TAG)


def nav(request):
    dlist = HardDisk.objects.all()
    for d in dlist:
        logger.info('\r\n' + str(d))
    context = {'DiskList': dlist}
    return render(request, 'navigation.html', context)


def gallery(request):
    one_page_count = 12
    page_num = request.GET.get('page', 1)

    query = '''
            SELECT * FROM MediaModel_media
            where imdb_id is not null and imdb_id!=''
            group by imdb_id
            order by i18n_title
            '''
    mlist = Media.objects.raw(query)

    view_list = []
    for media in mlist:
        view_dict = {}
        view_dict['id'] = media.id
        view_dict['year'] = media.release_date.year
        view_dict['disk'] = media.disk_sn
        view_dict['path'] = media.path
        view_dict['i18n_title'] = media.get_i18n_title()
        view_dict['title'] = media.get_title()
        view_dict['imdb_id'] = media.get_imdb_id()
        if not media.image_paths == '':
            try:
                view_dict['poster'] = eval(media.image_paths)[Static.KEY_IMAGE_CATEGORY_POSTER][1:]
            except SyntaxError as e:
                logger.error(e)
        if 'poster' not in view_dict or view_dict['poster'] == '':
            view_dict['poster'] = '/static/images/no-image.png'
        view_list.append(view_dict)

    pager = Paginator(view_list, one_page_count)

    # 获取当前页的数据
    try:
        page_data = pager.page(page_num)
    except PageNotAnInteger:
        # 返回第一页的数据
        page_data = pager.page(1)
    except EmptyPage:
        # 返回最后一页的数据
        page_data = pager.page(pager.num_pages)
    context = {'PageData': page_data}
    if request.method == 'POST':
        return render(request, 'gallery.html', context)
    else:
        return render(request, 'image.html', context)


def movie_windows(request):
    database_id = request.GET.get('id', 1)
    movie = Media.objects.filter(Q(id=database_id))[0]

    view_dict = {}
    view_dict['id'] = movie.id
    view_dict['year'] = movie.release_date.year
    view_dict['disk'] = movie.disk_sn
    view_dict['path'] = movie.path
    view_dict['i18n_title'] = movie.get_i18n_title()
    view_dict['title'] = movie.get_title()
    view_dict['imdb_id'] = movie.get_imdb_id()
    if not movie.image_paths == '':
        try:
            view_dict['poster'] = eval(movie.image_paths)[Static.KEY_IMAGE_CATEGORY_POSTER][1:]
        except SyntaxError as e:
            logger.error(e)
    if 'poster' not in view_dict or view_dict['poster'] == '':
        view_dict['poster'] = '/static/images/no-image.png'

    context = {'movie': view_dict}
    if request.method == 'POST':
        return render(request, 'window_modal_movie.html', context)
    else:
        return HttpResponse('error')
