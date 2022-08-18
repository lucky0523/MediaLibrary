import json
import logging

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from MediaModel.models import Media
from MediaLibrary.common import Static

LOG_TAG = '[WebPage.views] '
logging.basicConfig(level=Static.LOG_LEVEL, format='%(asctime)s - %(name)s %(levelname)s - %(message)s')
logger = logging.getLogger(LOG_TAG)


def imgs(request):
    # img_list = models.Img.objects.all()
    one_page_count = 12
    page_num = request.GET.get('page', 1)

    view_list = []
    mlist = Media.objects.filter(~Q(imdb_id=''))
    # mlist = mlist[one_page_count * (page_num - 1):one_page_count * page_num]
    for media in mlist:
        view_dict = {}
        view_dict['year'] = media.release_date.year
        view_dict['disk'] = media.disk_sn
        view_dict['path'] = media.path
        view_dict['title'] = media.get_i18n_title()
        if not media.image_paths == '':
            try:
                view_dict['image'] = eval(media.image_paths)[Static.KEY_IMAGE_CATEGORY_POSTER][1:]
            except SyntaxError as e:
                logger.error(e)
        if 'image' not in view_dict or view_dict['image'] == '':
            view_dict['image'] = '/static/images/no-image.png'
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
    return render(request, 'image.html', context)
