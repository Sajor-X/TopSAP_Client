# TopSAP_Client
天融信VPN客户端

> 官方应用有繁杂的验证码输入，且频繁断连，此项目使用OCR框架，识别验证码，且自动检测vpn链接状态，断连则自动重连。

OCR项目：https://github.com/Sajor-X/AutoLogin

## 打包

### Windows

> pyinstaller -F manager.py -i favicon.ico -w

### MacOS

> pyinstaller -F manager.py -i favicon.ico -p . --add-data "env.ini:." -w


## 可执行文件

### Windows

TopSAP_Client.exe 为Windows可执行程序，需搭配env.ini使用


### MacOS 

修改好env.ini 文件后需要放到路径： ~/.top/env.ini

mkdir -p ~/.top
cp -rf ./env.ini ~/.top

