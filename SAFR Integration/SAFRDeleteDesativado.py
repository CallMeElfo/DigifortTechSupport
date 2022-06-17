#!/usr/bin/python3

from datetime import datetime
import time
import logging
import os
import cv2
import requests
import base64
import json
import shutil
from PIL import Image, ImageEnhance

logging.basicConfig(filename='app.log', filemode='w',level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.getLogger().addHandler(logging.StreamHandler())

BASE_URL = 'http://localhost:8080{0}'
user_id = ''
passwd = ''
directory = 'main'
site=''
source = ''

def createHeader(user_id, password, directory):
    enconding = 'utf-8'
    encode_password =  base64.b64encode(bytes(password, enconding)).decode(enconding)
    header_auth = "{0}:{1}".format(user_id, encode_password)
    return {
        'Content-Type': 'application/octet-stream',
        'X-RPC-AUTHORIZATION' : header_auth,
        'X-RPC-DIRECTORY' : directory
    }

extId = '42'
covi_url = base_url+'/people/external/'+str(extId)
person_id = requests.get(covi_url, (header = createHeader(user_id, passwd, directory)))
print (person_id)
covi_url = base_url+'/people/'+str(person_id)

http_response = requests.delete(url = covi_url, headers=headers)

if http_response.status_code == 204:
    print("Person deleted")
elif http_response.status_code == 400:
    print("Person not found")
else:
    print("Error")
