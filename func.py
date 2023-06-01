import os 

def timestamp(e):
    e = int(e)
    t = str(int(e)) + "秒"
    if 60 <= int(e):
        n = int(e) % 60
        o = int(e / 60)
        t = str(o) + "分" + str(n) + "秒"
        if 60 <= o:
            o = int(e / 60) % 60
            s = int(int(e / 60) / 60)
            t = str(s) + "小时" + str(o) + "分" + str(n) + "秒"
            if 24 <= s:
                s = int(int(e / 60) / 60) % 24
                t = str(int(int(int(e / 60) / 60) / 24)) + "天" + str(s) + "小时" + str(o) + "分" + str(n) + "秒"
    return t

def timestamp_to_str(seconds):
    seconds = int(seconds)
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    result = ""
    if days > 0:
        result += f"{days}天"
    if hours > 0:
        result += f"{hours}小时"
    if minutes > 0:
        result += f"{minutes}分"
    result += f"{seconds}秒"

    return result

 
def calc_recv_send(size):
    if size < 1024:
        size = str(size) + "B"
    elif size >= 1024 and size < 1024*1024:
        size = "{:.2f}".format(size / 1024) + "KB"
    elif size >= 1024*1024 and size < 1024*1024*1024:
        size = "{:.2f}".format(size / (1024*1024)) + "MB"
    elif size >= 1024*1024*1024 and size < 1024*1024*1024*1024:
        size = "{:.2f}".format(size / (1024*1024*1024)) + "GB"
    else:
        size = "{:.2f}".format(size / (1024*1024*1024*1024)) + "TB"
    return size





async def check_network():
    try:
        await asyncio.create_subprocess_exec('ping', '-c', '1', '172.38.80.214')
        print("网络通畅")
        return True
    except subprocess.CalledProcessError:
        print("网络不通畅")
        return False

check_network()

