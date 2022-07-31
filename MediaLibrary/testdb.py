# -*- coding: utf-8 -*-
import json
import logging
import os.path
from pathlib import Path
from django.http import HttpResponse

import MediaModel.utils
from MediaModel.models import Media
from MediaLibrary.common import StaticKey
from MediaLibrary.query import douban

LOG_TAG = '[testdb] '
logging.basicConfig(level=StaticKey.LOG_LEVEL, format='%(asctime)s - %(name)s %(levelname)s - %(message)s')
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
    add_list = content[StaticKey.KEY_ADD_LIST]
    disk_sn = content[StaticKey.KEY_CONFIG_DISK_SN]
    for media_info in add_list:
        logger.info(media_info)
        test1 = Media(disk_sn=disk_sn)
        test1.compile(media_info)
        logger.info(test1)
    f.close()
    return HttpResponse('bbb')