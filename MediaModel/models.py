import logging
import os

from django.core.exceptions import ValidationError
from django.db import models

import MediaModel.utils
from MediaLibrary.common import Static
from MediaLibrary.query import InfoQuery

LOG_TAG = '[MediaModel.models] '
logging.basicConfig(level=Static.LOG_LEVEL, format='%(asctime)s - %(name)s %(levelname)s - %(message)s')
logger = logging.getLogger(LOG_TAG)


# Create your models here.
class Media(models.Model):
    imdb_id = models.CharField(max_length=32)
    douban_id = models.CharField(max_length=32)
    tmdb_id = models.CharField(max_length=32)
    douban_read = models.BooleanField(default=False)
    local_read = models.BooleanField(default=False)
    title = models.CharField(max_length=200, default="", null=True, blank=True)
    i18n_title = models.CharField(max_length=200, default="", null=True, blank=True)
    language = models.CharField(max_length=32, default="", null=True, blank=True)
    director = models.CharField(max_length=32, default="", null=True, blank=True)
    actor = models.CharField(max_length=32, default="", null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    disk_sn = models.CharField(max_length=32, default="", null=True, blank=True)
    path = models.TextField(default="", null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    file_size = models.FloatField(default=0)
    subtitle = models.CharField(max_length=32, default="", null=True, blank=True)
    image_paths = models.TextField(default="", null=True, blank=True)
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
                    self.release_date,
                    self.disk_sn,
                    self.path,
                    self.get_media_type_display(),
                    self.get_file_type_display(),
                    self.file_size)

    def get_i18n_title(self):
        i_title = 'Error i18n title'
        try:
            i_title = eval(self.i18n_title)[Static.LANGUAGE]  # eval()用以将json字符串转为字典
        except SyntaxError as e:
            logger.error('Get i18n title error')
            logger.error(e)
        return i_title

    def get_title(self):
        title = 'Error title'
        try:
            title = self.title
        except SyntaxError as e:
            logger.error('Get title error')
            logger.error(e)
        return title

    def get_imdb_id(self):
        title = 'Error title'
        try:
            title = self.imdb_id
        except SyntaxError as e:
            logger.error('Get title error')
            logger.error(e)
        return title

    def match(self):
        print(self.path)
        if self.imdb_id == '':
            media_name = os.path.basename(self.path)
            key_word, year = MediaModel.utils.return_keyword(media_name)
            info_result = InfoQuery.auto_match_movie(key_word, year)
            print('xxxx')
            if info_result:
                try:
                    self.imdb_id = info_result.imdb_id
                    self.tmdb_id = info_result.tmdb_id
                    self.title = info_result.title
                    self.i18n_title = info_result.i18n_title
                    self.language = info_result.language
                    self.director = info_result.director
                    self.actor = info_result.actor
                    self.release_date = info_result.release_date
                    self.media_type = info_result.media_type
                    self.save()
                except ValidationError as e:
                    logger.error(e)
            else:
                logger.info('Cannot match this: ' + self.path)
                pass
        else:
            logger.info('Matched, title: ' + self.get_i18n_title())

    # def download_images(self):
    #     image_paths_dict = {}
    #     try:
    #         if self.image_paths != '':
    #             image_paths_dict = eval(self.image_paths)
    #     except SyntaxError:
    #         logger.error('Image path eval error: ' + self.image_paths)
    #     for image_category in Static.KEY_IMAGE_CATEGORIES:
    #         if image_category not in image_paths_dict \
    #                 or image_paths_dict[image_category] == '' \
    #                 or not os.path.exists(image_paths_dict[image_category]):
    #             image_paths_dict[image_category] = InfoQuery.get_movie_image(self.imdb_id, image_category)
    #             self.image_paths = str(image_paths_dict)
    #             self.save()
    #         else:
    #             logger.info('Images exist.')

    def download_images(self):
        logger.info('Start download [%s %s] images.' % (self.get_i18n_title(), self.imdb_id))
        image_dir = Static.PATH_FILMS_IMAGES + str(self.imdb_id) + '/'
        image_paths_dict = {}
        need_download_categories = []
        need_save = False
        try:
            if self.image_paths != '':
                image_paths_dict = eval(self.image_paths)
        except SyntaxError:
            logger.error('Image path eval error: ' + self.image_paths)
        if os.path.isdir(image_dir):
            logger.info('Folder is exists. Check files.')
            for image_category in Static.KEY_IMAGE_CATEGORIES:
                if image_category in image_paths_dict and os.path.isfile(image_paths_dict[image_category]):
                    logger.info('[%s] file exists and matched' % image_category)
                    pass
                else:
                    logger.info('[%s] file not matched' % image_category)
                    image_exists = False
                    for sub_path in os.scandir(image_dir):
                        if image_category == os.path.basename(sub_path).split('.')[0]:
                            logger.info('[%s] file found, replace it.' % os.path.basename(sub_path))
                            image_exists = True
                            need_save = True
                            image_paths_dict[image_category] = image_dir + os.path.basename(sub_path)
                            break
                    if not image_exists:
                        need_download_categories.append(image_category)

        else:
            logger.info('Folder is not exists. Download all!')
            need_download_categories = Static.KEY_IMAGE_CATEGORIES.copy()

        if need_download_categories.__len__() > 0:
            need_save = True
            logger.info('Need download: %s.' % need_download_categories)
            for image_category in need_download_categories:
                logger.info('Download %s of "%s".' % (image_category, self.get_i18n_title()))
                image_paths_dict[image_category] = InfoQuery.get_movie_image(self.imdb_id, image_category)

        if need_save:
            self.image_paths = str(image_paths_dict)
            self.save()
        else:
            logger.info('Download [%s %s] images: Nothing has changed.' % (self.get_i18n_title(), self.imdb_id))
