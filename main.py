import json
import os
import logging
import platform
import sys
from enum import Enum
from os.path import join, getsize

LOG_TAG = '[MediaCollect] '
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s %(levelname)s - %(message)s')
logger = logging.getLogger(LOG_TAG)

KEY_CONFIG_FOLDER = 'media_folder'
KEY_CONFIG_DISK_NAME = 'disk_name'
KEY_CONFIG_DISK_SPACE = 'disk_space'
KEY_CONFIG_DISK_SN = 'disk_sn'

KEY_PATH = 'm_path'
KEY_TYPE = 'm_type'
KEY_SIZE = 'm_size'
KEY_ADD_LIST = 'add_list'
KEY_DEL_LIST = 'del_list'


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
    canonical_path = path.path[path.path.find(config[KEY_CONFIG_FOLDER]):]
    size = calc_size(path)
    media_list.append({KEY_PATH: canonical_path, KEY_TYPE: m_type.value, KEY_SIZE: size})
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


if __name__ == '__main__':
    app_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    logger.info('Working at ' + app_path)
    if platform.system() == 'Windows':
        root_path = app_path.split(':\\')[0] + ':\\'
        config = read_config(app_path)
        media_path = root_path + config[KEY_CONFIG_FOLDER]
        result_list = []
        scan_media(media_path, result_list)
        logger.info('Scan done! Found ' + str(result_list.__len__()) + ' media files.')
        upload_content = {
            KEY_CONFIG_DISK_NAME: config[KEY_CONFIG_DISK_NAME],
            KEY_CONFIG_DISK_SN: config[KEY_CONFIG_DISK_SN],
            KEY_ADD_LIST: result_list,
        }
        print(upload_content)
        f = open(app_path + 'r.txt', 'w')
        f.write(json.dumps(upload_content, sort_keys=True, indent=4, separators=(',', ': ')))
        f.close()
