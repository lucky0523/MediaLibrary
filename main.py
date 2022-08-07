import json
import os
import logging
import platform
import sys
from enum import Enum
from os.path import join, getsize

import requests

import Static

LOG_TAG = '[MediaCollect] '
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s %(levelname)s - %(message)s')
logger = logging.getLogger(LOG_TAG)

_base_url = 'http://192.168.1.120:8000'


class FileType(Enum):
    NOT = 0
    Bluray = 1
    Remux = 2
    Web = 3


config = {}


def read_config(path):
    f = open(path + '/conf.json', encoding='utf-8')
    text = f.read()
    f.close()
    logger.info('Get config:\r\n' + text)
    config = json.loads(text)
    return config


# The unit of return value is MB
def calc_size(path):
    size = 0.0
    if path.is_dir():
        for root, dirs, files in os.walk(path):
            size += sum([getsize(join(root, name)) for name in files])
    else:
        size = getsize(path)
    return round(size / 1048576, 2)


def is_media_file(file_name):
    return file_name.lower().endswith(('.mkv', '.mp4', 'iso'))


def media_list_append(media_list, path, m_type):
    canonical_path = path.path[path.path.find(config[Static.KEY_CONFIG_FOLDER]):]
    size = calc_size(path)
    media_list.append({Static.KEY_PATH: canonical_path, Static.KEY_TYPE: m_type.value, Static.KEY_SIZE: size})
    logger.info('Add a media, path:' + canonical_path + ', type:' + str(m_type) + ', size:' + str(size) + 'MB.')


def scan_media(path, media_list):
    for sub_path in os.scandir(path):
        sub_path_name = sub_path.name.lower()
        if sub_path.is_dir():
            if sub_path_name == 'bdmv':
                media_list_append(media_list, path, FileType.Bluray)
                break
            else:
                scan_media(sub_path, media_list)
        elif sub_path.is_file() and is_media_file(sub_path_name):
            if sub_path_name.__contains__('web-dl'):
                media_list_append(media_list, sub_path, FileType.Web)
            elif sub_path_name.endswith('.iso'):
                media_list_append(media_list, sub_path, FileType.Bluray)
            else:
                media_list_append(media_list, sub_path, FileType.Remux)


def upload(content_json):
    response = requests.post(url=_base_url + '/upload/', json=content_json)
    logger.info(response.text)
    return response.text


if __name__ == '__main__':
    app_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    logger.info('Working at ' + app_path)
    if platform.system() == 'Windows':
        root_path = app_path.split(':\\')[0] + ':\\'
        config = read_config(app_path)
        media_path = root_path + config[Static.KEY_CONFIG_FOLDER]
        result_list = []
        scan_media(media_path, result_list)
        logger.info('Scan done! Found ' + str(result_list.__len__()) + ' media files.')
        upload_content = {
            Static.KEY_API_VERSION: Static.API_VERSION,
            Static.KEY_CONFIG_DISK_VENDOR: config[Static.KEY_CONFIG_DISK_VENDOR],
            Static.KEY_CONFIG_DISK_SERIES: config[Static.KEY_CONFIG_DISK_SERIES],
            Static.KEY_CONFIG_DISK_SPACE: config[Static.KEY_CONFIG_DISK_SPACE],
            Static.KEY_CONFIG_DISK_SN: config[Static.KEY_CONFIG_DISK_SN],
            Static.KEY_ADD_LIST: result_list,
        }
        print(upload_content)
        upload(upload_content)
        # f = open(app_path + '\\r.txt', 'w')
        # f.write(json.dumps(upload_content, sort_keys=True, indent=4, separators=(',', ': ')))
        # f.close()
