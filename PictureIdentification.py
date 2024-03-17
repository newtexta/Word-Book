import requests 
import base64
import os
def basic_identification_high(image):
    a = os.path.abspath('.')
    b = a.split("\\")
    c = tuple(b)
    d = '/'.join(c)
    I_S_path = d + "/resource/Identification.txt"
    with open(I_S_path,"r") as f:
        all_ = f.readlines()
        APP_ID = all_[0][3:-1]
        APP_SECRET = all_[1][7:-1]
    host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={APP_ID}&client_secret={APP_SECRET}'
    response = requests.get(host)
    if response:
        access_token = response.json()["access_token"]
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    f = open(image, 'rb')
    img = base64.b64encode(f.read())
    params = {"image":img}
    access_token = response.json()["access_token"]
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        results = response.json()['words_result']
        print(results)
        return results
def basic_identification_standard(image):
    a = os.path.abspath('.')
    b = a.split("\\")
    c = tuple(b)
    d = '/'.join(c)
    I_S_path = d + "/resource/Identification.txt"
    with open(I_S_path,"r") as f:
        all_ = f.readlines()
        APP_ID = all_[0][3:-1]
        APP_SECRET = all_[1][7:-1]
    host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={APP_ID}&client_secret={APP_SECRET}'
    response = requests.get(host)
    if response:
        access_token = response.json()["access_token"]
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    f = open(image, 'rb')
    img = base64.b64encode(f.read())
    params = {"image":img}
    access_token = response.json()["access_token"]
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        results = response.json()["words_result"]
        print(results)
        return results