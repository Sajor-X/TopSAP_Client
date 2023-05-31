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
