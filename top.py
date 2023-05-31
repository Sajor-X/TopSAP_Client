from retrying import retry
 
import time
import requests
import base64
import json
import logging
import configparser
import warnings
from requests.packages import urllib3
# 关闭警告
urllib3.disable_warnings()
warnings.filterwarnings("ignore")



class AutoLoginTopSap():
    def __init__(self, host, port, username, password, ocr):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.client_host = "https://localhost:7443/api"
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.code_url = self.client_host + "/v1/get_gid?serverAddr=111.33.112.66&serverPort=10443&vpn_version=ngvone&auth_protocol=0&auth_port=10443&data_port=10443&data_protocol=0&cert_type=0&proxyType=&proxyAddr=&proxyPort=&proxyUser=&proxyPwd=&proxyDomain=&rnd=0.21450320730512473"
        self.auto_code_url = ocr
        self.logout_url = self.client_host + "/v1/logout"
        self.login_url = self.client_host + "/v1/login_by_pwd"
        self.config_info_url = self.client_host + "/v1/get_config_info"
        self.query_statistics_url = self.client_host + "/v1/query_statistics"
        self.session = requests.session()
        self.json_headers = {
            'Content-Type': 'application/json'
        }
        self.form_headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

    
    def get_code_img(self):
        """
        获取验证码图片
        """
        response = self.session.get(self.code_url, verify=False)
        with open('result.png', 'wb') as f:
            f.write(response.content)
        return response.content
    
    def get_code_base64(self, content):
        """
        返回base64图片文本
        """
        return "data:image/png;base64," + base64.b64encode(content).decode('utf-8')
        

    def get_code_text(self):
        """
        获取验证码Code
        """
        result = self.get_code_base64(self.get_code_img())
        data = {
            "base64": result,
            "name": "erp",
            "threshold": 0,
            "count": 0
        }

        code = self.session.post(self.auto_code_url, headers=self.json_headers, data=json.dumps(data), verify=False).text
        return code

    def query_statistics(self):
        """
        统计连接数据
        """
        data = {"method": "query_statistics"}
        response = self.session.post(self.query_statistics_url, headers=self.json_headers, data=json.dumps(data), verify=False).json()

        terr_code = response.get('terr_code') # != 0 

        return response
    
    def get_config_info(self):
        data = {"method": "get_config_info"}
        response = self.session.post(self.config_info_url, headers=self.json_headers, data=json.dumps(data), verify=False).json()
        return response
    
    def logout(self):
        """
        登出
        """
        data = {"method":"logout"}
        response = self.session.post(self.logout_url, headers=self.json_headers, data=json.dumps(data), verify=False).text
        return response
    
    @retry(stop_max_attempt_number=10)
    def login(self):
        code = self.get_code_text()
        """
        自动登陆
        """
        data = {
            "method": "login_by_pwd",
            "vone": { 
                "addr": self.host, 
                "port": self.port,
                "user": base64.b64encode(self.username.encode('utf-8')).decode('utf-8'),

                "pwd": base64.b64encode(self.password.encode('utf-8')).decode('utf-8')
            },
            "proxy": { 
                "type":"",
                "addr":"",
                "port":"",
                "user":"",
                "pwd":"",
                "domain":""
            },
            "gid" : { 
                "cgid":"" ,
                "gid": code 
            } ,
            "vpn_version" :"ngvone",
            "auth_protocol":"0" ,
            "auth_port": "10443" ,
            "data_port": "10443" ,
            "data_protocol": "0" ,
            "cert_type": "0" ,
            "remember_pwd": "off" 
        }
        response = self.session.post(self.login_url, headers=self.json_headers, data=json.dumps(data), verify=False).json()
        if response.get('err_code') != 0:
            if response.get('err_code') == -18:
                self.logout()
            raise Exception("Login failed")
        print("登录成功")
        return response
    
    def listen(self):
        while True:
            try:
                stat = self.query_statistics()
                if stat.get('terr_code') != 0 or stat.get('session_id') == '':
                    self.login()
            except Exception as e:
                print(e)
                pass
            time.sleep(1)
            return stat 
             

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('env.ini')

    env = config.get('ENV', 'env')

    host = config.get(env, 'host')
    port = config.get(env, 'port')
    username = config.get(env, 'username')
    password = config.get(env, 'password')
    ocr = config.get(env, 'ocr_url')

    app = AutoLoginTopSap(host, port, username, password, ocr)
    print(app.get_config_info())

