import json
import logging
import time

from django.http import HttpResponse
from django.shortcuts import render

from MediaModel.models import Media
from MediaLibrary.common import Static

LOG_TAG = '[MediaModel.views] '
logging.basicConfig(level=Static.LOG_LEVEL, format='%(asctime)s - %(name)s %(levelname)s - %(message)s')
logger = logging.getLogger(LOG_TAG)


def hello(request):
    context = {}
    context['hello'] = 'Hello World!'
    context['name'] = 'xxxx'
    context['pic'] = '/static/films_folder/tt2379713/post.webp'
    return render(request, 'demo.html', context)


def upload(request):
    f = open('./static/r.txt', 'r')
    text = f.read()
    content = json.loads(text)
    add_list = content[Static.KEY_ADD_LIST]
    disk_sn = content[Static.KEY_CONFIG_DISK_SN]
    for media_info in add_list:
        logger.info(media_info)
        test1 = Media(disk_sn=disk_sn,
                      file_size=media_info[Static.KEY_SIZE],
                      file_type=media_info[Static.KEY_TYPE],
                      path=media_info[Static.KEY_PATH])
        logger.info(test1)
        test1.save()
    f.close()
    return HttpResponse('bbb')


def match(request):
    mlist = Media.objects.all()
    logger.info('Start match info: Found ' + str(mlist.__len__()) + ' Media.')
    # 输出所有数据
    for model in mlist:
        time.sleep(1)
        model.match()
    return HttpResponse('match')


def refresh_images(request):
    mlist = Media.objects.all()
    logger.info('Start refresh images: Found ' + str(mlist.__len__()) + ' Media.')
    # 输出所有数据
    for model in mlist:
        model.download_images()
        model.save()
    return HttpResponse('images')
