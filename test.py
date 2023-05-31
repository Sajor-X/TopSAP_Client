
import os, tkinter as tk
from SysTrayIcon import SysTrayIcon

class _Main:  # 调用SysTrayIcon的Demo窗口
    def __init__(s):
        s.SysTrayIcon = None  # 判断是否打开系统托盘图标

    def main(s):
        # tk窗口
        s.root = tk.Tk()
        s.root.bind("<Unmap>", # Unmap表示隐藏时触发
                    lambda event: s.Hidden_window() if s.root.state() == 'iconic' else False)  # 窗口最小化判断，可以说是调用最重要的一步
        s.root.protocol('WM_DELETE_WINDOW', s.exit)  # 点击Tk窗口关闭时直接调用s.exit，不使用默认关闭
        s.root.resizable(0, 0)  # 锁定窗口大小不能改变
        s.root.geometry("800x500")
        s.root.title("手机远程调试工具V1.0_By:亓乐")
        s.root.mainloop()


    def switch_icon(s, _sysTrayIcon, icon='D:\\2.ico'):
        # 点击右键菜单项目会传递SysTrayIcon自身给引用的函数，所以这里的_sysTrayIcon = s.sysTrayIcon
        # 只是一个改图标的例子，不需要的可以删除此函数
        _sysTrayIcon.icon = icon
        _sysTrayIcon.refresh()

        # 气泡提示的例子
        s.show_msg(title='图标更换', msg='图标更换成功！', time=500)

    def show_msg(s, title='标题', msg='内容', time=500):
        s.SysTrayIcon.refresh(title=title, msg=msg, time=time)

    def Hidden_window(s, icon='D:\\1.ico', hover_text="SysTrayIcon.py Demo"):
        '''隐藏窗口至托盘区，调用SysTrayIcon的重要函数'''

        # 托盘图标右键菜单, 格式: ('name', None, callback),下面也是二级菜单的例子
        # 24行有自动添加‘退出’，不需要的可删除
        menu_options = (('一级 菜单', None, s.switch_icon),
                        ('二级 菜单', None, (('更改 图标', None, s.switch_icon),)))

        s.root.withdraw()  # 隐藏tk窗口
        if not s.SysTrayIcon: s.SysTrayIcon = SysTrayIcon(
            icon,  # 图标
            hover_text,  # 光标停留显示文字
            menu_options,  # 右键菜单
            on_quit=s.exit,  # 退出调用
            tk_window=s.root,  # Tk窗口
        )
        s.SysTrayIcon.activation()

    def exit(s, _sysTrayIcon=None):
        s.root.destroy()
        print('exit...')


if __name__ == '__main__':
    Main = _Main()



    Main.main()

