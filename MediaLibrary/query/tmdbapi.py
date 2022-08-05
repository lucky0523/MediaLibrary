import logging
import os

import requests
from MediaLibrary.common import Static

LOG_TAG = '[MediaModel.query.tmdbapi] '
logging.basicConfig(level=Static.LOG_LEVEL, format='%(asctime)s - %(name)s %(levelname)s - %(message)s')
logger = logging.getLogger(LOG_TAG)

_urls = {
    "movie_search": "/search/movie",
    "movie_detail": "/movie/",
    "movie_images": "/movie/",
}

_base_url = 'https://api.themoviedb.org/3'
_image_base_url = 'https://image.tmdb.org/t/p/original'
_api_key = "a7283cc765063ff22da2fdd86d999745"


def search_movie(keyword, year=-1, page=1):
    params = {'api_key': _api_key,
              'language': Static.LANGUAGE,
              'query': keyword,
              'page': page
              }
    if year != -1:
        params.update({'year': year})
    x = requests.get(url=_base_url + _urls['movie_search'], params=params)
    return x.json()


def get_movie_detail(mid):
    params = {'api_key': _api_key,
              'language': Static.LANGUAGE,
              }
    x = requests.get(url=_base_url + _urls['movie_detail'] + str(mid), params=params)
    return x.json()


def get_movie_image(mid):
    params = {'api_key': _api_key,
              'language': Static.LANGUAGE,
              'include_image_language': 'en,null',
              }
    x = requests.get(url=_base_url + _urls['movie_images'] + str(mid) + '/images', params=params)
    return x.json()


def download_image(remote_path, dest_dir, filename):
    logger.info('Start download image: ' + _image_base_url + remote_path)
    os.makedirs(dest_dir, exist_ok=True)
    r = requests.get(_image_base_url + remote_path)
    local_path = dest_dir + '/' + filename + '.' + remote_path.split('.')[-1]
    with open(local_path, 'wb') as f:
        f.write(r.content)  # 写入二进制内容
        f.close()
    return local_path
