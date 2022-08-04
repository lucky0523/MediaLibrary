# -*- coding: utf-8 -*-
import json
import logging
import os.path
import time
from pathlib import Path
from django.http import HttpResponse

import MediaModel.utils
from MediaModel.models import Media
from MediaLibrary.common import Static
from MediaLibrary.query import doubanapi

LOG_TAG = '[testdb] '
logging.basicConfig(level=Static.LOG_LEVEL, format='%(asctime)s - %(name)s %(levelname)s - %(message)s')
logger = logging.getLogger(LOG_TAG)


# 数据库操作
def testdb(request):
    test1 = Media(douban_id='firstmovie')
    test1.save()
    return HttpResponse("<p>数据添加成功！</p>")


# 数据库操作
def read_db(request):
    # 初始化
    response = ""
    response1 = ""

    # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
    list = Media.objects.all()

    # 输出所有数据
    for var in list:
        response1 += var.douban_id + " "
    response = response1
    return HttpResponse("<p>" + response + "</p>")


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
    return HttpResponse('images')
