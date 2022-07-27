import os
import platform
import sys
from enum import Enum
from os.path import join, getsize


class file_type(Enum):
    NOT = 0
    Bluray = 1
    Remux = 2
    Web = 3


media_folder = '\\Movies'


# The unit of return value is MB
def calc_size(path):
    size = 0.0
    if path.is_dir():
        for root, dirs, files in os.walk(path):
            size += sum([getsize(join(root, name)) for name in files])
            size = size / 1048576
    else:
        size = getsize(path) / 1048576
    return round(size, 2)


def is_media_file(file_name):
    return file_name.lower().endswith(('.mkv', '.mp4', 'iso'))


def scan_media(path, media_list):
    for sub_path in os.scandir(path):
        print(type(sub_path))
        print(sub_path)
        sub_path_name = sub_path.name.lower()
        if sub_path.is_dir():
            if sub_path_name == 'bdmv':
                media_list.append((path.path, file_type.Bluray, calc_size(path)))
                break
            else:
                scan_media(sub_path, media_list)
        elif sub_path.is_file() and is_media_file(sub_path_name):
            if sub_path_name.__contains__('web-dl'):
                media_list.append((sub_path.path, file_type.Web, calc_size(sub_path)))
            elif sub_path_name.endswith('.iso'):
                media_list.append((sub_path.path, file_type.Bluray, calc_size(sub_path)))
            else:
                media_list.append((sub_path.path, file_type.Remux, calc_size(sub_path)))


def traversal_files(path):
    for i in os.scandir(path):
        print(i)
        if i.is_dir():
            traversal_files(i)


if __name__ == '__main__':
    app_path = os.path.realpath(sys.argv[0])
    if platform.system() == 'Windows':
        root_path = app_path.split(':\\')[0] + ':\\'
        movie_path = root_path + media_folder
        print(movie_path)
        result_list = []
        scan_media(movie_path, result_list)
        print(result_list)
