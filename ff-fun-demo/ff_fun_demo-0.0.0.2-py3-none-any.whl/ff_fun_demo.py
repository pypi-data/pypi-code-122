import datetime
from fake_useragent import UserAgent
import sys
import time
import hashlib
import requests
import urllib3
class operation_list(object):
    '''列表操作功能'''
    def division_list(list,nub):
        '''分割列表
        list:为列表
        nub:分割数量'''
        list_name=[]
        if len(list)%nub==0:
            for i in range(0,len(list),int(len(list)/nub)):
                name = list[i:i + int(len(list)/nub)]
                list_name.append(name)
        else:
            for i in range(0,len(list),int(len(list)/nub)+1):
                name = list[i:i + int(len(list)/nub)+1]
                list_name.append(name)
        return      list_name
class operation_time(object):
    '''时间操作功能'''
    def getfronttime(beforeOfDay):
        '''向前偏移
        beforeOfDay:偏移天数'''
        today = datetime.datetime.now()
            # 计算偏移量
        offset = datetime.timedelta(days=-beforeOfDay)
                # 获取想要的日期的时间
        re_date = (today + offset).strftime('%Y-%m-%d')
        return re_date
    def getaftertime(day):
        '''当时时间天数向后偏移
        day:偏移天数'''
        today = datetime.datetime.now()
        # 计算偏移量
        offset = datetime.timedelta(days=day)
        # 获取修改后的时间并格式化
        re_date = (today + offset).strftime('%Y-%m-%d %H:%M:%S')
        return re_date
class   operation_Reptile(object):
    '''爬虫操作'''
    def getUa():
        '''获取随机UA'''
        try:
            ua = UserAgent()
            user_agent = ua.random
            return user_agent
        except Exception as e:
            pass
    def proxy_ip(orderno,secret):
        '''讯代理动态ip
        IP为代理服务器地址
        auto为协议头
        orderno = "ZF20179xxxxxxxxx"
        secret = "3f9c2ecac7xxxxxxxxxxxxxxxx"'''
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        _version = sys.version_info

        is_python3 = (_version[0] == 3)

       

        ip = "forward.xdaili.cn"
        port = "80"

        ip_port = ip + ":" + port

        timestamp = str(int(time.time()))              
        string = ""
        string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp

        if is_python3:                          
            string = string.encode()

        md5_string = hashlib.md5(string).hexdigest()                
        sign = md5_string.upper()                             
        #print(sign)
        auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp
        return {"IP":ip_port,"auth":auth}    
if __name__ == '__main__':
    print(operation_Reptile.getUa())

       


