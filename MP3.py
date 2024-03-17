import requests
import json
import time
import re
import os
def download_audio_gb(word):
    folder = 'gb_mp3'
    if not os.path.exists(folder):
        os.makedirs(folder)
    url = f"https://ssl.gstatic.com/dictionary/static/sounds/oxford/{word}--_gb_1.mp3"
    response = requests.get(url)
    if response.status_code == 200:
        filepath = os.path.join(folder, f"{word}.mp3")
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"{word} gb download success")
        state1 = "gb_ok"
    else:
        print(f"{word} gb download failed")
        state1 = "gb_no"
    return word,state1
def download_audio_us(word):
    folder = 'us_mp3'
    if not os.path.exists(folder):
        os.makedirs(folder)
    url = f"https://ssl.gstatic.com/dictionary/static/sounds/oxford/{word}--_us_1.mp3"
    response = requests.get(url)
    if response.status_code == 200:
        filepath = os.path.join(folder, f"{word}.mp3")
        with open(filepath, 'wb') as f:
            f.write(response.content)
        state2 = "us_ok"
        print(f"{word} us download success")
    else:
        state2 = "us_no"
        print(f"{word} us download failed")
    return word,state2
def gb_audio_state(word):
    url = f"https://ssl.gstatic.com/dictionary/static/sounds/oxford/{word}--_gb_1.mp3"
    response = requests.get(url)
    if response.status_code == 200:
        state = "ok"
    else:
        state = "no"
    return state
def us_audio_state(word):
    url = f"https://ssl.gstatic.com/dictionary/static/sounds/oxford/{word}--_us_1.mp3"
    response = requests.get(url)
    if response.status_code == 200:
        state = "ok"
    else:
        state = "no"
    return state