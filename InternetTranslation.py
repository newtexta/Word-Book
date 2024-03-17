import requests
import hashlib
import random
import os
def translation(q,from_lang,to_lang):
    a = os.path.abspath('.')
    b = a.split("\\")
    c = tuple(b)
    d = '/'.join(c)
    T_S_path = d + "/resource/Translation.txt"
    with open(T_S_path,"r") as f:
        all_ = f.readlines()
        APP_ID = all_[0][3:-1]
        APP_SECRET = all_[1][7:-1]
    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    appid = APP_ID
    secret_key = APP_SECRET
    salt = random.randint(32768, 65536)
    sign_str = appid + q + str(salt) + secret_key
    sign = hashlib.md5(sign_str.encode()).hexdigest()
    params = {
        'q': q,
        'from': from_lang,
        'to': to_lang,
        'appid': appid,
        'salt': salt,
        'sign': sign
    }
    response = requests.get(url, params=params)
    result = response.json()
    if 'trans_result' in result:
        translation = result['trans_result'][0]['dst']
        return translation
    else:
        translation = "翻译失败"
        return translation