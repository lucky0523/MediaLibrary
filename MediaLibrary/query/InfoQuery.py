import logging

from MediaLibrary.common import GlobleParam
from MediaLibrary.common import Static
from MediaLibrary.query import tmdbapi
from MediaLibrary.query import doubanapi

LOG_TAG = '[MediaModel.query.InfoQuery] '
logging.basicConfig(level=Static.LOG_LEVEL, format='%(asctime)s - %(name)s %(levelname)s - %(message)s')
logger = logging.getLogger(LOG_TAG)


class InfoResult:
    imdb_id = ''
    douban_id = 0
    tmdb_id = 0
    title = ''
    i18n_title = {}
    language = ''
    director = ''
    actor = ''
    release_date = ''
    media_type = 0


def auto_match_movie(keyword, year=-1):
    info_result = InfoResult()
    if GlobleParam.g_search_api == Static.KEY_TMDB_API:
        query_result = search_movie(keyword, year)
        if 'total_results' in query_result and query_result['total_results'] > 0:
            lucky_one = query_result['results'][0]
            lucky_detail = get_movie_detail(lucky_one['id'])
            logger.info('Lucky result: ' + str(lucky_detail))
            info_result.imdb_id = lucky_detail['imdb_id']
            info_result.tmdb_id = lucky_detail['id']
            info_result.title = lucky_detail['original_title']
            info_result.i18n_title[Static.LANGUAGE] = lucky_detail['title']
            info_result.language = lucky_detail['original_language']
            info_result.release_date = lucky_detail['release_date']
            return info_result
        else:
            return info_result
    elif GlobleParam.g_search_api == Static.KEY_DOUBAN_API:
        return info_result


def search_movie(keyword, year=-1, page=1):
    if GlobleParam.g_search_api == Static.KEY_TMDB_API:
        return tmdbapi.search_movie(keyword, year, page)
        pass
    elif GlobleParam.g_search_api == Static.KEY_DOUBAN_API:
        pass


def get_movie_detail(mid):
    if GlobleParam.g_search_api == Static.KEY_TMDB_API:
        return tmdbapi.get_movie_detail(mid)
        pass
    elif GlobleParam.g_search_api == Static.KEY_DOUBAN_API:
        pass


def get_movie_image(mid, image_category):
    file_path = ''
    if GlobleParam.g_search_api == Static.KEY_TMDB_API:
        result = tmdbapi.get_movie_image(mid)
        image_list = result[image_category + 's']
        if image_list.__len__() > 0:
            file_path = tmdbapi.download_image(image_list[0]['file_path'], Static.PATH_FILMS_IMAGES + mid + '/',
                                               image_category)
    elif GlobleParam.g_search_api == Static.KEY_DOUBAN_API:
        pass
    return file_path
