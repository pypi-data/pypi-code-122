import time

import requests

from tsdl.core.context import Context
from tsdl.api import app, acc, em, pro
from tsdl.logger.log import logger

"""
    测试中常用操作命令
"""


def send(context: Context, data: dict, retry_times: int = 3):
    """
    发送操作命令 - 向测试端app
    :param context:         上下文
    :param data:            发送数据
    :param retry_times:     失败重试次数（默认：3次）
    :return:
    """
    try:
        logger.info('SEND-> client:{} data:{}'.format(context.url, data))
        result = app.send(context.url, data)
        logger.info('SEND<- result:{}'.format(result))
    except requests.exceptions.MissingSchema as me:
        logger.error(str(me))
        raise AssertionError(str(me))
    except ConnectionError as ce:
        logger.error(str(ce))
        sleep(context, 10)
        retry_times -= 1
        if retry_times <= 0:
            raise AssertionError(str(ce))
        else:
            send(context, data, retry_times)

    return result


def sleep(context: Context, seconds: int):
    """
    休眠
    :param context:     上下文
    :param seconds:     秒
    :return:
    """
    logger.info('SLEEP {}secs'.format(seconds))
    time.sleep(seconds)


def encode(context: Context, parse: dict):
    """
    协议组帧
    :param context:     上下文
    :param parse:       组帧数据
    :return:
    """
    logger.info('ENCODE-> parse:{}'.format(parse))
    frame = pro.encode(parse)
    logger.info('ENCODE<- frame:{}'.format(frame))

    return frame


def decode(context: Context, frame: str, session: None):
    """
    协议解帧
    :param context:     上下文
    :param frame:       数据帧
    :param session:     会话 - 加解密信息
    :return:
    """
    logger.info('DECODE-> frame:{} session:{}'.format(frame, session))
    parse = pro.decode(frame, session)
    logger.info('DECODE<- parse:{}'.format(parse))

    return parse


def manual(context: Context, protocol: str, operation: str, security: str = None):
    """
    协议组帧帮助
    :param context:     上下文
    :param protocol:    协议（如：GW698 | DLMS 等）
    :param operation:   操作
    :param security:    安全
    :return:
    """
    logger.info('ENCODE MANUAL-> operation:{} security:{}'.format(operation, security))
    result = pro.manual(protocol=protocol, operation=operation, security=security)
    logger.info('ENCODE MANUAL<- result:{}'.format(result))

    return result


def compare(context: Context, name: str, data: dict):
    """
    比对、计算和验证数据
    :param context:     上下文
    :param name:        比对关键字
    :param data:        比对数据
    :return:
    """
    logger.info('COMPARE-> name:{} data:{}'.format(name, data))
    result = acc.accept(name, data)
    logger.info('COMPARE<- result:{}'.format(result))
    return result


def framing(context: Context, name: str, data: dict):
    """
    分帧处理
    :param context:
    :param name:
    :param data:
    :return:
    """
    pass


def api(context: Context, name: str, data: dict):
    """
    调用用户自定义服务api
    :param context:
    :param name:
    :param data:
    :return:
    """
    pass


def execute(context: Context, **args):
    """
    执行语句
    语句类型:
        1. 赋值
        2. 判断或处理逻辑等
    :param context:     上下文
    :param args:        执行语句
    :return:
    """
    for expr in args:
        exec(expr)


"""
    测试中结果判断命令
"""


def diagnose(context: Context, condition: str, success_msg: str, error_msg: str):
    """
    断言 - 失败，程序会停止运行
    :param context:         上下文
    :param condition:       条件
    :param success_msg:     成功返回信息
    :param error_msg:       错误返回信息
    :return:
    """
    if eval(condition):
        logger.info('DIAGNOSE-> condition:{} result:{}'.format(condition, True))
        send(context, {'app:show': {'msg': success_msg}})
    else:
        logger.info('DIAGNOSE-> condition:{} result:{}'.format(condition, False))
        send(context, {'app:show': {'msg': error_msg}})
        raise AssertionError(error_msg)


def presume(context: Context, condition: str, success_msg: str, error_msg: str):
    """
    假定 - 失败，程序不会停止运行
    :param context:         上下文
    :param condition:       条件
    :param success_msg:     成功返回信息
    :param error_msg:       错误返回信息
    :return:
    """
    if eval(condition):
        logger.info('PRESUME-> condition:{} result:{}'.format(condition, True))
        send(context, {'app:show': {'msg': success_msg}})
    else:
        logger.info('PRESUME-> condition:{} result:{}'.format(condition, False))
        send(context, {'app:show': {'msg': error_msg}})


"""
    测试中调用加密机命令
"""


def negotiate(context: Context, meter_esam_sn: str, meter_esam_counter: int):
    """
    协商
    :param context:                 上下文
    :param meter_esam_sn:           电表ESAM序列号
    :param meter_esam_counter:      电表ESAM计数器
    :return:
    """
    logger.info('NEGOTIATE-> esam_sn:{} esam_counter:{}'.format(meter_esam_sn, meter_esam_counter))
    result = em.negotiate(meter_esam_sn, meter_esam_counter)
    logger.info('NEGOTIATE<- result:{}'.format(result))

    return result


def verify(context: Context, em_rn: str, meter_esam_sn: str, meter_esam_rn: str, meter_esam_mac: str):
    """
    验证
    :param context:                 上下文
    :param em_rn:                   加密机随机数
    :param meter_esam_sn:           电表ESAM序列号
    :param meter_esam_rn:           电表ESAM随机数
    :param meter_esam_mac:          电表ESAM MAC
    :return:
    """
    logger.info('VERIFY-> em_rn:{} esam_sn:{} esam_rn:{} esam_mac:{}'.format(em_rn, meter_esam_sn, meter_esam_rn,
                                                                             meter_esam_mac))
    result = em.verify_session(em_rn, meter_esam_sn, meter_esam_rn, meter_esam_mac)
    logger.info('VERIFY<- result:{}'.format(result))

    return result
