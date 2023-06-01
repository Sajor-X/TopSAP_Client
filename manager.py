import tkinter as tk
import configparser
from top import AutoLoginTopSap
from func import timestamp, timestamp_to_str, calc_recv_send
import sys
import os


class AutoLoginApp:
    def __init__(self, host, port, username, password, ocr):
        self.auto_login = AutoLoginTopSap(host, port, username, password, ocr)
        self.icon_path = os.path.join(sys.path[0], 'favicon.ico')

        self.root = tk.Tk()
        self.root.title("VPN")
        self.root.geometry("300x200")
        self.root.resizable(False, False)

        # 创建变量
        self.connection_status = tk.StringVar()
        self.connection_recv = tk.StringVar()
        self.update_tunnel_duration()

        # 创建标签
        self.status_label = tk.Label(self.root, textvariable=self.connection_status)
        self.recv_label = tk.Label(self.root, textvariable=self.connection_recv)

        self.status_label.grid(row=0, column=0)
        self.recv_label.grid(row=0, column=1)


        # 创建菜单栏
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # 创建菜单
        self.menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="重新登陆", command=self.retry_login)
        

        # 创建托盘图标
        # self.create_tray_icon()
        self.root.iconbitmap(self.icon_path)

    def retry_login(self):

        # 重新登陆
        self.auto_login.logout()
        self.auto_login.login()


    def update_tunnel_duration(self):
        stat = self.auto_login.query_statistics()
        print(stat)
        if stat.get('terr_code') != 0 or stat.get('session_id') == '':
            self.auto_login.login()
        else:
            tunnel_duration = stat.get('tunnel_duration')
            self.connection_status.set("已连接时长：" + timestamp_to_str(tunnel_duration))

            recv_bytes = stat.get('recv_bytes')
            send_bytes = stat.get('send_bytes')
            self.connection_recv.set("↓" + calc_recv_send(recv_bytes) + " / ↑" + calc_recv_send(send_bytes))
        self.root.after(1000, self.update_tunnel_duration)
            

    def run(self):
        # 运行主循环
        self.root.mainloop()

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('env.ini')

    env = config.get('ENV', 'env')

    host = config.get(env, 'host')
    port = config.get(env, 'port')
    username = config.get(env, 'username')
    password = config.get(env, 'password')
    ocr = config.get(env, 'ocr_url')

    app = AutoLoginApp(host, port, username, password, ocr)
    app.run()
