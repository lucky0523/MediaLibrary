import logging
import os
import re

import requests

from MediaLibrary.common import Static

LOG_TAG = '[MediaModel.utils]'
logging.basicConfig(level=Static.LOG_LEVEL, format='%(asctime)s - %(name)s %(levelname)s - %(message)s')
logger = logging.getLogger(LOG_TAG)

SPLIT_SYMBOLS = ['uhd', '1080p', 'bluray', 'blu-ray', 'repack', 'ultrahd']


def return_keyword(file_name):
    cut_position = split_file_name(file_name)
    raw_title = file_name[:cut_position - 1]
    # word_list = raw_title.split('.' or ' ')
    print(file_name)
    word_list = re.split('[. \s]', raw_title)
    print(word_list)
    year = -1

    for i in range(len(word_list) - 1, -1, -1):
        if word_list[i].isdecimal():
            if 1900 < int(word_list[i]) < 2030:
                year = int(word_list[i])
                for j in range(len(word_list) - i):
                    word_list.pop(i)
                break
    if year == -1:
        logger.info('Not found "year" at "' + raw_title + '"')
    key_word = ' '.join(word_list)
    logger.debug('File name: ' + file_name + '. Raw title: ' + raw_title + '. Keyword: ' + key_word)
    return key_word, year


def split_file_name(file_name):
    file_name = file_name.lower()
    min_position = 9999
    for symbol in SPLIT_SYMBOLS:
        index = file_name.find(symbol)
        if index != -1:
            min_position = min(min_position, index)
    return min_position
