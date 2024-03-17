from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, QThread, Signal
import time
import psutil
import socket
import requests
import multiprocessing
from multiprocessing import freeze_support
class Internet(QThread):
    host_name_S = Signal(str, str, str, str, str, str, str)
    def run(self):
        last_total_bytes_sent = 0
        last_total_bytes_recv = 0
        try:
            hostname = socket.gethostname()
            ip_addressZ = socket.gethostbyname(hostname)
            host_name = "主机名 : " + hostname
            response = requests.get('https://api.ipify.org')
            ip_address = response.text
            response = requests.get(f'http://ip-api.com/json/{ip_address}?lang=zh-CN')
            geo_info = response.json()
            country, region, city = geo_info["country"], geo_info['regionName'], geo_info["city"]
            cpu_cores = multiprocessing.cpu_count()
            cpu_coreS = str(cpu_cores)
            in_ip = "本机内网IP地址：" + ip_addressZ
            if ip_address:
                out_ip = "本机公网 IP 地址：" + ip_address
                ip_address = "IP 地址归属地：" + country + ' ' + region + ' ' + city
            else:
                out_ip = "None"
                ip_address = "无法获取公网IP，可能由于没有连接网络，请检查网络状态！"
            cpu_num = "CPU核心数：" + cpu_coreS
        except:
            pass
        while True:
            new_total_bytes_sent = psutil.net_io_counters().bytes_sent
            new_total_bytes_recv = psutil.net_io_counters().bytes_recv
            upload_speed = new_total_bytes_sent - last_total_bytes_sent
            download_speed = new_total_bytes_recv - last_total_bytes_recv
            if upload_speed >= 1024:
                upload_speed = upload_speed / 1024
                D = "KB"
                if upload_speed >= 1024:
                    upload_speed = upload_speed / 1024
                    D = "MB"
                    if upload_speed >= 1024:
                        upload_speed = upload_speed / 1024
                        D = "GB"
            else:
                D = "B"
            if download_speed >= 1024:
                download_speed = download_speed / 1024
                D = "KB"
                if download_speed >= 1024:
                    download_speed = download_speed / 1024
                    D = "MB"
                    if download_speed >= 1024:
                        download_speed = download_speed / 1024
                        D = "GB"
            else:
                D = "B"
            upload_speed_text = "上传速度: {:.2f} {}/s".format(upload_speed,D)
            download_speed_text = "下载速度: {:.2f} {}/s".format(download_speed,D)
            last_total_bytes_sent = new_total_bytes_sent
            last_total_bytes_recv = new_total_bytes_recv
            self.host_name_S.emit(host_name, in_ip, out_ip, ip_address, download_speed_text, upload_speed_text, cpu_num)
            time.sleep(1)