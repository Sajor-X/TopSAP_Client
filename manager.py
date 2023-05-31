import tkinter as tk
import configparser
from top import AutoLoginTopSap
from func import timestamp, timestamp_to_str
from PIL import Image, ImageTk
import sys
import os
import win32gui
import win32con
import win32api


class AutoLoginApp:
    def __init__(self, host, port, username, password, ocr):
        self.auto_login = AutoLoginTopSap(host, port, username, password, ocr)
        self.icon_path = os.path.join(sys.path[0], 'favicon.ico')

        self.root = tk.Tk()
        self.root.title("连接状态")
        self.root.geometry("300x200")
        self.root.resizable(False, False)

        # 创建变量
        self.connection_status = tk.StringVar()
        self.update_tunnel_duration()

        # 创建标签
        self.status_label = tk.Label(self.root, textvariable=self.connection_status)
        self.status_label.pack(pady=20)
        # 创建按钮
        self.minimize_button = tk.Button(self.root, text="最小化", command=self.minimize_to_tray)
        self.minimize_button.pack(pady=10)

        # 创建托盘图标
        self.create_tray_icon()
        self.root.iconbitmap(self.icon_path)

    def minimize_to_tray(self):
        # 最小化窗口到托盘
        self.root.withdraw()
        self.tray_icon.visible = True

    def create_tray_icon(self):
        # 创建托盘图标
        
        self.nid = (self.root.winfo_id(), 0, win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP, win32con.WM_USER + 20, win32gui.LoadIcon(0, win32con.IDI_APPLICATION), "AutoLoginApp")
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, self.nid)

        def on_tray_click(hwnd, msg, wparam, lparam):
            if lparam == win32con.WM_LBUTTONUP:
                self.restore_window()
            elif lparam == win32con.WM_RBUTTONUP:
                menu = win32gui.CreatePopupMenu()
                win32gui.AppendMenu(menu, win32con.MF_STRING, 1024, '打开')
                win32gui.AppendMenu(menu, win32con.MF_STRING, 1025, '退出')
                pos = win32gui.GetCursorPos()
                win32gui.SetForegroundWindow(self.root.winfo_id())
                win32gui.TrackPopupMenu(menu, win32con.TPM_LEFTALIGN, pos[0], pos[1], 0, hwnd, None)
                win32gui.PostMessage(hwnd, win32con.WM_NULL, 0, 0)

        win32gui.SetWindowLong(self.root.winfo_id(), win32con.GWL_WNDPROC, on_tray_click)

    def restore_window(self):
        # 从托盘还原窗口
        self.root.deiconify()
        self.tray_icon.visible = False

    def exit_app(self):
        # 退出应用程序
        self.root.quit()

    def minimize_window(self):
        # 最小化窗口到任务栏
        self.root.iconify()
        

    def update_tunnel_duration(self):
        stat = self.auto_login.query_statistics()
        if stat.get('terr_code') != 0 or stat.get('session_id') == '':
            self.auto_login.login()
        tunnel_duration = stat.get('tunnel_duration')

        self.connection_status.set("已连接时长：" + timestamp_to_str(tunnel_duration))
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
