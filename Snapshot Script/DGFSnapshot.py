import configparser
import requests
import time
from collections import defaultdict
from datetime import date
import os
from os import path

#Load Config
cameraRegisterDict = {}
config = configparser.ConfigParser()
config.read('settings.ini')
for camera in config.sections():
    cameraRegisterDict[camera] = {}
    cameraRegisterDict[camera]['user'] = config[camera]['user']
    cameraRegisterDict[camera]['password'] = config[camera]['password']
    cameraRegisterDict[camera]['address'] = config[camera]['address']
    cameraRegisterDict[camera]['APIport'] = config[camera]['APIport']
    cameraRegisterDict[camera]['cameraName'] = config[camera]['cameraName']

#Downlaod Image
def downloadImage(user, password, address, APIport, cameraName):
    url = 'http://{}:{}@{}:{}/Interface/Cameras/GetSnapshot?Camera={}&ResponseFormat=JSON'.format(user, password, address, APIport, cameraName)
    data = requests.get(url, timeout=10)
    if not path.isdir(cameraName):
        os.mkdir(cameraName)
    cameraDirectory = ((os.path.dirname(os.path.abspath(__file__)) + '\\' + cameraName + '\\' + str(cameraName) + str(date.today()) + ".jpg"))
    print (cameraDirectory)
    with open(cameraDirectory, 'wb') as f:
        f.write(data.content)


for server in cameraRegisterDict:
    user = cameraRegisterDict[camera]['user']
    password = cameraRegisterDict[camera]['password']
    address = cameraRegisterDict[camera]['address']
    APIport = cameraRegisterDict[camera]['APIport']
    cameraName = cameraRegisterDict[camera]['cameraName']
    downloadImage(user, password, address, APIport, cameraName)
