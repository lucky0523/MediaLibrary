import json
import logging
import time

from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q

from MediaModel.models import Media
from HardDiskModel.models import HardDisk
from MediaLibrary.common import Static

LOG_TAG = '[MediaModel.views] '
logging.basicConfig(level=Static.LOG_LEVEL, format='%(asctime)s - %(name)s %(levelname)s - %(message)s')
logger = logging.getLogger(LOG_TAG)


def receive(request):
    print(request.method)
    response_text = ''
    if request.method == 'POST':
        add_count = 0
        string = str(request.body, 'utf-8')
        content = json.loads(string)
        print(content)
        try:
            if content[Static.KEY_API_VERSION] != Static.API_VERSION:
                response_text = 'Version is not match. Server version:%s. Client version:%s.' \
                                % (Static.API_VERSION, content[Static.KEY_API_VERSION])
                logger.info(response_text)
            else:
                add_list = content[Static.KEY_ADD_LIST]
                disk_sn = content[Static.KEY_CONFIG_DISK_SN]
                for media_info in add_list:
                    logger.info(media_info)
                    if Media.objects.filter(disk_sn=disk_sn, path=media_info[Static.KEY_PATH]).__len__() == 0:
                        media = Media(disk_sn=disk_sn,
                                      file_size=media_info[Static.KEY_SIZE],
                                      file_type=media_info[Static.KEY_TYPE],
                                      path=media_info[Static.KEY_PATH])
                        logger.info(media)
                        media.save()
                        add_count += 1
                print(add_list)
                print(disk_sn)
                response_text = 'Done! Add ' + str(add_count) + ' raw media info.'
        except KeyError as e:
            logger.error(e)
            response_text = 'KeyError Occurred, not found [%s]' % e
    else:
        response_text = 'Error: Only handle POST request.'
    return HttpResponse(response_text)


def match(request):
    mlist = Media.objects.filter(imdb_id='')
    logger.info('Start match info: Found ' + str(mlist.__len__()) + ' Media.')
    # 输出所有数据
    length = mlist.__len__()
    for i in range(length):
        logger.info('Handle %d/%d, path: %s' % (i + 1, length, mlist[i].path))
        # time.sleep(1)
        mlist[i].match()
    return HttpResponse('match')


def refresh_images(request):
    mlist = Media.objects.filter(~Q(imdb_id=''))
    logger.info('Start refresh images: Found ' + str(mlist.__len__()) + ' Media.')
    length = mlist.__len__()
    for i in range(length):
        logger.info('Handle %d/%d, path: %s' % (i + 1, length, mlist[i].path))
        # time.sleep(1)
        mlist[i].download_images()
    return HttpResponse('images')


def test_local(request):
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


def add_hard_disk(request):
    hard_disk = HardDisk(vendor='WD', series='Elements', sn='9KGE9JNL', capacity=14)
    hard_disk.save()
    return HttpResponse('hhhh')
