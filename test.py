
    # def minimize_to_tray(self):
    #     # 最小化窗口到托盘
    #     self.root.withdraw()
    #     self.tray_icon.visible = True

    # def create_tray_icon(self):
    #     # 创建托盘图标
        
    #     self.nid = (self.root.winfo_id(), 0, win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP, win32con.WM_USER + 20, win32gui.LoadIcon(0, win32con.IDI_APPLICATION), "AutoLoginApp")
    #     win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, self.nid)

    #     def on_tray_click(hwnd, msg, wparam, lparam):
    #         if lparam == win32con.WM_LBUTTONUP:
    #             self.restore_window()
    #         elif lparam == win32con.WM_RBUTTONUP:
    #             menu = win32gui.CreatePopupMenu()
    #             win32gui.AppendMenu(menu, win32con.MF_STRING, 1024, '打开')
    #             win32gui.AppendMenu(menu, win32con.MF_STRING, 1025, '退出')
    #             pos = win32gui.GetCursorPos()
    #             win32gui.SetForegroundWindow(self.root.winfo_id())
    #             win32gui.TrackPopupMenu(menu, win32con.TPM_LEFTALIGN, pos[0], pos[1], 0, hwnd, None)
    #             win32gui.PostMessage(hwnd, win32con.WM_NULL, 0, 0)

    #     win32gui.SetWindowLong(self.root.winfo_id(), win32con.GWL_WNDPROC, on_tray_click)

    # def restore_window(self):
    #     # 从托盘还原窗口
    #     self.root.deiconify()
    #     self.tray_icon.visible = False

    # def exit_app(self):
    #     # 退出应用程序
    #     self.root.quit()

    # def minimize_window(self):
    #     # 最小化窗口到任务栏
    #     self.root.iconify()
        


