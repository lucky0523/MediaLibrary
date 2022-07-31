import logging
import os

from django.db import models

import MediaModel.utils
from MediaLibrary.common import StaticKey
from MediaLibrary.query import douban

LOG_TAG = '[MediaModel.models] '
logging.basicConfig(level=StaticKey.LOG_LEVEL, format='%(asctime)s - %(name)s %(levelname)s - %(message)s')
logger = logging.getLogger(LOG_TAG)


# Create your models here.
class Media(models.Model):
    imdb_id = models.CharField(max_length=32)
    douban_id = models.CharField(max_length=32)
    tmdb_id = models.CharField(max_length=32)
    title = models.CharField(max_length=200, default="", null=True, blank=True)
    douban_read = models.BooleanField(default=False)
    local_read = models.BooleanField(default=False)
    director = models.CharField(max_length=32, default="", null=True, blank=True)
    actor = models.CharField(max_length=32, default="", null=True, blank=True)
    year = models.IntegerField(default=0)
    disk_sn = models.CharField(max_length=32, default="", null=True, blank=True)
    path = models.CharField(max_length=100, default="", null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    file_size = models.FloatField(default=0)
    subtitle = models.CharField(max_length=32, default="", null=True, blank=True)
    resolution_enum = (
        (1, '2K'),
        (2, '4K')
    )
    resolution = models.SmallIntegerField(choices=resolution_enum, default=0)
    media_type_enum = (
        (0, 'N/A'),
        (1, 'Movie'),
        (2, 'TV'),
        (3, 'Documentary'),
    )
    media_type = models.SmallIntegerField(choices=media_type_enum, default=0)
    file_type_enum = (
        (0, 'N/A'),
        (1, 'Bluray'),
        (2, 'Remux'),
        (3, 'Web')
    )
    file_type = models.SmallIntegerField(choices=file_type_enum, default=0)

    def __int__(self, disk_sn):
        self.disk_sn = disk_sn
        logger.debug('xxxxxxxx' + disk_sn)

    def __str__(self):
        return 'Title:{}\r\nYear:{}\r\nDisk_SN:{}\r\nPath:{}\r\nMedia type:{}\r\nFile type:{}\r\nSize:{}MB' \
            .format(self.title,
                    self.year,
                    self.disk_sn,
                    self.path,
                    self.media_type,
                    self.get_file_type_display(),
                    self.get_media_type_display())

    def compile(self, media_info):
        self.file_size = media_info[StaticKey.KEY_SIZE]
        self.file_type = media_info[StaticKey.KEY_TYPE]
        print('xxxx' + str(media_info[StaticKey.KEY_TYPE]))
        print('yyyy' + str(self.file_type))
        self.path = media_info[StaticKey.KEY_PATH]
        media_name = os.path.basename(self.path)
        key_word = MediaModel.utils.return_keyword(media_name)
        search_result = douban.search(key_word)
        if search_result['total'] > 0:
            douban_info = search_result['items'][0]
            logger.debug(douban_info)
