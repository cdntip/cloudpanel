


# 分页
def Pagination(page, limit, dataLen=999):
    if page == 1 or page == 0:
        return 0, limit
    a = int(limit) * int(page)
    if dataLen < int(limit):
        return 0, a
    return a - int(limit), a


def DateTimeToStr(_datetime):
    try:
        return _datetime.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return str(_datetime)

def is_ipv4(ip: str) -> bool:
   return True  if [1] * 4 == [x.isdigit() and 0 <= int(x) <= 255 for x in ip.split(".")] else False


def md5(str):
    import hashlib
    m2 = hashlib.md5()
    m2.update(str.encode("utf-8"))
    return m2.hexdigest()


def traffic_format(traffic):
    if traffic < 1024 * 8:
        return str(int(traffic)) + "B"

    if traffic < 1024 * 1024:
        return str(round((traffic / 1024.0), 1)) + "KB"

    if traffic < 1024 * 1024 * 1024:
        return str(round((traffic / (1024.0 * 1024)), 1)) + "MB"

    if traffic < 1024 * 1024 * 1024 * 1024 * 1024:
        return str(round((traffic / (1024.0 * 1024 * 1024 * 1024)), 1)) + "PB"

    return str(round((traffic / 1073741824.0), 1)) + "GB"

if __name__ == '__main__':
    print('Hello CDNTIP')