import json

import requests
from datetime import datetime

_user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.20(0x18001434) NetType/WIFI Language/en"
_headers = {'User-Agent': _user_agent,
            'Referer': 'https://servicewechat.com/wx2f9b06c1de1ccfca/84/page-frame.html',
            'Accept-Encoding': 'gzip,compress,deflate',
            'content-type': 'application/json'}
_api_key = "0ac44ae016490db2204ce0a042db2916"
_base_url = "https://frodo.douban.com/api/v2"

ts = datetime.strftime(datetime.now(), '%Y%m%d')

params = {'apiKey': _api_key}
params.update({'q': 'Terminal 2019', 'start': 0, 'count': 20, '_ts': ts})
print(params)
x = requests.get(url=_base_url + "/search/movie", params=params, headers=_headers)

# 返回 json 数据

print(json.dumps(x.json(), sort_keys=True, indent=4, separators=(',', ': ')))
