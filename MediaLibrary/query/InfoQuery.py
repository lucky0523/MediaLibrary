import logging

from MediaLibrary.common import GlobleParam
from MediaLibrary.common import StaticKey
from MediaLibrary.query import tmdbapi
from MediaLibrary.query import doubanapi

LOG_TAG = '[MediaModel.query.InfoQuery] '
logging.basicConfig(level=StaticKey.LOG_LEVEL, format='%(asctime)s - %(name)s %(levelname)s - %(message)s')
logger = logging.getLogger(LOG_TAG)


class InfoResult:
    imdb_id = 0
    douban_id = 0


def auto_match_movie(model, keyword, year=-1):
    if GlobleParam.g_search_api == StaticKey.KEY_TMDB_API:
        query_result = search_movie(keyword, year)
        if 'total_results' in query_result and query_result['total_results'] > 0:
            lucky_result = query_result['results'][0]
            logger.info('Lucky result: ' + str(lucky_result))
            model.tmdb_id = lucky_result['id']
            model.title = lucky_result['original_title']
            model.i18n_title = lucky_result['title']
            model.language = lucky_result['original_language']
            return True
        else:
            pass
    elif GlobleParam.g_search_api == StaticKey.KEY_DOUBAN_API:
        pass


def search_movie(keyword, year=-1, page=1):
    if GlobleParam.g_search_api == StaticKey.KEY_TMDB_API:
        return tmdbapi.search_movie(keyword, year, page)
        pass
    elif GlobleParam.g_search_api == StaticKey.KEY_DOUBAN_API:
        pass
