import requests
from MediaLibrary.common import StaticKey

_urls = {
    "movie_search": "/search/movie",
}

_base_url = 'https://api.themoviedb.org/3'
_api_key = "a7283cc765063ff22da2fdd86d999745"


def search_movie(keyword, year=-1, page=1):
    params = {'api_key': _api_key,
              'language': StaticKey.LANGUAGE,
              'query': keyword,
              'page': page
              }
    if year != -1:
        params.update({'year': year})
    x = requests.get(url=_base_url + _urls['movie_search'], params=params)
    return x.json()
