import socket

from tsdl.api import mm
from tsdl.common import util


class Context(object):
    """
    测试用例上下文
    """

    def __init__(self, script: str, url: str, *loops):
        self._script = script
        if script is None:
            raise Exception('Path of script file is null.')
        pfs = script.split('.')
        pfs[-1] = pfs[-1] + '.py'
        if not util.pathUtil.exist(*pfs):
            raise Exception('Script file[{}] is not exist.'.format(script))

        self._url = url
        if not util.is_valid_url(url):
            raise Exception('Format of app url is not right that should be http://IP:PORT/accept.')

        self._loops = []
        if len(loops) > 0:
            for data in loops:
                self._loops.append(Loop(data))

        self._runtime = Runtime()
        self._cache = Cache(self)

    @property
    def script(self):
        return self._script

    @property
    def url(self):
        return self._url

    @property
    def loops(self):
        return self._loops

    @property
    def runtime(self):
        return self._runtime

    @property
    def cache(self):
        return self._cache


class Loop(object):
    def __init__(self, data: dict):
        r = data.get('range')
        if r is None:
            raise Exception('Can not find range in loops. It should be like "start:end".')
        if r.find(':') <= 0:
            raise Exception('Format of range value is not right. It should be like "start:end"')
        self._range = Range(r)

        self._count = data.get('count')
        if self._count is None:
            raise Exception('Can not find count in loops. It should be decimal like 1, 2...')
        if self._count <= 0:
            raise Exception('Count must be more then 0.')

    @property
    def range(self):
        return self._range

    @property
    def count(self):
        return self._count


class Range(object):
    def __init__(self, value: str):
        self._list = value.split(':')
        if len(self._list) != 2:
            raise Exception('Length of range value after split must be 2.')
        if not self._list[0].isdigit():
            raise Exception('Fist number of range must be decimal.')
        self._start = int(self._list[0])
        if not self._list[1].isdigit():
            raise Exception('Fist number of range must be decimal.')
        self._end = int(self._list[1])
        if self._start > self._end:
            raise Exception('Fist number of range must be less than second number of range.')

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end


class Runtime(object):
    """
    运行时
    """
    def __init__(self):
        self._step = None
        self._loop_times = None
        self._total_loop_times = None
        self._last_result = None

    def reset_loop(self):
        self._loop_times = None
        self._total_loop_times = None

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, value):
        self._step = value

    @property
    def last_result(self):
        return self._last_result

    @last_result.setter
    def last_result(self, value):
        self._last_result = value

    @property
    def loop_times(self):
        return self._loop_times

    @loop_times.setter
    def loop_times(self, value):
        self._loop_times = value

    @property
    def total_loop_times(self):
        return self._total_loop_times

    @total_loop_times.setter
    def total_loop_times(self, value):
        self._total_loop_times = value


class Cache(object):
    """
    缓存
    """
    def __init__(self, context: Context):
        self._context = context
        self._name = '{}:cache'.format(socket.gethostname())

    def get(self, key: str):
        """
        获取键值key对应的数据从缓存中
        :param key:
        :return:
        """

        return mm.get(self._name, key)

    def set(self, key: str = None, data=None, mapping: dict = None):
        """
        保存运行时数据到缓存中
        :param key:
        :param data:
        :param mapping:
        :return:
        """
        if key is not None:
            mm.put(self._name, key, data)
        else:
            for k, v in mapping.items():
                mm.put(self._name, k, v)

    def delete(self, key: str = None):
        """
        删除缓存中运行时数据
        :param key:
        :return:
        """

        return mm.delete(self._name, key)


class App(object):
    def __init__(self, context: Context):
        self._context = context
        self._name = 'app:manual'

    def command(self, key: str, **kwargs):
        """
        获取APP的command数据
        :param key:
        :return:
        """
        command = util.replace(mm.get(self._name, key),
                               step_no=util.extract_digit(self._context.runtime.step))

        return util.replace(command, **kwargs)

        # data = {
        #     "meter_pos": "#METER_POSITION",
        #     "step_no": "#STEP_NO",
        #     "todo": {
        #         "meter:comm": {
        #             "msg": "#MSG",
        #             "channel": {
        #                 "name": "#CHANNEL_NAME",
        #                 "braudrate": "#BRAUDRATE"
        #             },
        #             "frame": "#COMM_FRAME"
        #         }
        #     }
        # }

        # "bench:power_off": {
        #     "msg": "#MSG",
        #     "Dev_Port": "#DEV_PORT"
        # }

        # "bench:adjust": {
        #     "msg": "修改表台输出...",
        #     "Phase": "context.meter.connect",
        #     "Rated_Volt": "context.meter.reference_voltage",
        #     "Rated_Curr": "context.meter.min_current",
        #     "Rated_Freq": 60,
        #     "PhaseSequence": 0,
        #     "Revers": 0,
        #     "Volt_Per": 100,
        #     "Curr_Per": 100,
        #     "IABC": "A",
        #     "CosP": 1.0,
        #     "SModel": "context.bench.model",
        #     "Dev_Port": 11
        # }

        # "bench:power_on": {
        #     "msg": "台体开始上电...",
        #     "Phase": "context.meter.connect",
        #     "Rated_Volt": "context.meter.reference_voltage",
        #     "Rated_Curr": "context.meter.min_current",
        #     "Rated_Freq": 60,
        #     "PhaseSequence": 0,
        #     "Revers": 0,
        #     "Volt_Per": 100,
        #     "Curr_Per": 100,
        #     "IABC": "A",
        #     "CosP": 1.0,
        #     "SModel": "context.bench.model",
        #     "Dev_Port": 11
        # }

        # {'app:show': {'msg': '抄读所有冻结数据开始...'}}
