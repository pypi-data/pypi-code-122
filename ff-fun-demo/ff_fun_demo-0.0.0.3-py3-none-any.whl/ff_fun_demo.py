import datetime
from fake_useragent import UserAgent
import sys
import time
import hashlib
import requests
import random
import urllib3
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
class Operation_list(object):
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
class Operation_time(object):
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
class   Operation_Reptile(object):
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
class   Operation_web(object):  
        '''Web后端操作'''
        def sendSms(accessKeyId, accessKeySecret,phone,SignName,TemplateCode,):
            '''阿里大于验证码短信发送
            6位数验证码
            accessKeyId:阿里大于keyid
            accessKeySecret:阿里大于keysecret
            phone:需要发送的手机号
            SignName:签名名字
            TemplateCode:短信模板'''
            try:
                client = AcsClient(accessKeyId, accessKeySecret, 'cn-hangzhou')

                request = CommonRequest()
                request.set_accept_format('json')
                request.set_domain('dysmsapi.aliyuncs.com')
                request.set_method('POST')
                request.set_protocol_type('https')  # https | http
                request.set_version('2017-05-25')
                request.set_action_name('SendSms')
                request.add_query_param('RegionId', 'cn-hangzhou')
                # 手机号码
                request.add_query_param('PhoneNumbers', phone)
                # 填写标记名称，将以【哈哈】显示在短信信息里
                request.add_query_param('SignName', SignName)
                # 模板的信息，在页面申请的模板信息里面查看
                request.add_query_param('TemplateCode', TemplateCode)
                # 发送的短信验证码123456，code是模板里${code}中的code，名称要相同
                serrcode = random.randint(100000, 999999)
                request.add_query_param('TemplateParam', '{"code":"' + str(serrcode) + '"}')
                response = client.do_action_with_exception(request)
                print(str(response, encoding='utf-8'))
                return {"state": 200, "msg": "发送成功",'serrcode':serrcode}
            except:
                return {"state": 404, "msg": "发送失败"}



if __name__ == '__main__':
    print(Operation_Reptile.getUa())

       


