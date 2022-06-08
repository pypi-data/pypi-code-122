from tsdl.logger.log import logger
from tsdl.core import interpret
from tsdl.core.context import Context


def run(script_path: str, app_url: str, *loops):
    """
    运行测试脚本
    :param script_path: 脚本代码文件存放包路径和脚本文件名[例如: script.abc.test]
    :param app_url: app访问url
    :param loops: 循环定义
    :return:
    """
    logger.info('TEST CASE START...')
    logger.info('run parameter -script_name "{}" -app_url "{}" -loops "{}"]'.format(script_path, app_url, loops))
    interpret.handle(Context(script_path, app_url, *loops))
    logger.info('TEST CASE END.')



