import logging
import re

from MediaLibrary.common import StaticKey

LOG_TAG = '[MediaModel.utils]'
logging.basicConfig(level=StaticKey.LOG_LEVEL, format='%(asctime)s - %(name)s %(levelname)s - %(message)s')
logger = logging.getLogger(LOG_TAG)

SPLIT_SYMBOLS = ['uhd', '1080p', 'bluray', 'blu-ray', 'repack']


def return_keyword(file_name):
    cut_position = split_file_name(file_name)
    raw_title = file_name[:cut_position - 1]
    word_list = raw_title.split('.')
    year = -1

    if word_list[-1].isdecimal():
        if 1900 < int(word_list[-1]) < 2030:
            year = int(word_list[-1])
            word_list.pop(-1)
    else:
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
