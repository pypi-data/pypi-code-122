import time
import datetime


def today():
    return datetime.date.today()


def str2date(ts, delimiter='-'):
    alter_ts = [1970, 1, 1]
    try:
        ts_tpl = [int(x) for x in ts.split(delimiter)[:3]]
        ts_tpl += alter_ts[len(ts_tpl):]
        return datetime.date(*ts_tpl)
    except:
        return datetime.date(*alter_ts)


def date2str(dt, fmt='%Y-%m-%d'):
    try:
        return dt.strftime(fmt)
    except:
        return datetime.date(1970, 1, 1).strftime(fmt)


def dtn():
    return datetime.datetime.now()


def now(fmt='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.now().strftime(fmt)


def str2unixtime(ts, fmt='%Y-%m-%d %H:%M:%S'):
    try:
        t = time.strptime(ts, fmt)
        return int(time.mktime(t))
    except Exception as _:
        print(_)


def unixtime2str(timestamp, fmt='%Y-%m-%d %H:%M:%S'):
    try:
        timestamp = time.localtime(timestamp)
        dt = time.strftime(fmt, timestamp)
        return dt
    except Exception as _:
        print(_)


def unixtime(mm=False):
    multi = 1000 if mm else 1
    return int(round(time.time() * multi))
