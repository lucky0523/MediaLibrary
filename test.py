import json
import os
import platform
import sys

curr_path = os.path.dirname(os.path.realpath(sys.argv[0]))
f = open(curr_path + '/conf.json', encoding='utf-8')
text = f.read()
f.close()
print(text)
config = json.loads(text)
print(config)
print(config['media_folder'])
print(type(config))
