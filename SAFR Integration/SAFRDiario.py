import requests
from requests.structures import CaseInsensitiveDict
import json
import base64
from datetime import datetime, timedelta

yesterday = datetime.today() - timedelta(days=1)
yesterday = yesterday.isoformat()
print (yesterday)

urlbase = ""
token = ''

url = (urlbase + '?data=' + str(yesterday))
headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Authorization"] = "Bearer {}".format(token)
response = requests.get(url, headers = headers, timeout = 500)
data = response.json()

i = 0

for key in data:

    situacao = data[i]['situacao']
    name = (data[i]['nome']) + '.png'
    b64string = data[i]['base64']
    while (len(b64string) % 4) != 0:
        b64string = b64string + '='
    b64string = b64string[22:]
    with  open(('.' + '\\' + situacao + "\\original\\" + name), 'wb') as b64img:
        b64img.write(base64.b64decode(b64string))
        b64img.close()
    i += 1
