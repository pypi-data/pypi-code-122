import importlib
import json
from nanoid import generate
from redis.client import StrictRedis
from redis.connection import ConnectionPool
from cloudam_stream.core.actors import Args, Actor, ComputeActor, SinkActor, SourceActor, ParallelComputeActor
from cloudam_stream.core.utils import base64_utils, dict_utils
from cloudam_stream.core.constants import actor_constant, config
from cloudam_stream.core.streams import RedisConsumer, RedisProducer
from cloudam_stream.core.utils.actor_utils import FlowStateUtils
from cloudam_stream.core.utils import serialize_inner
import pickle
import os


''' 
异步处理每个actor(除了SourceActor)的process，并实时判断actor是否应该结束，只处理一个port对应一个上游actor的情况
'''


class StreamApp(object):

    def __init__(self, actor: Actor):
        self.actor = actor
        self.actor_id: str = None
        self.upstream_actors_states = {}
        self.current_actor_state: str = actor_constant.ACTOR_STATE_READY
        self.current_actor_name: str = None
        self.redis_client: StrictRedis = None
        self.flow_depth: int = None
        self.actor_level: int = None
        self.state_manager: FlowStateUtils = None
        self.parallel_index: int = None

    def check_failed(self, upstream_actors):
        all_failed = True
        for upstream_actor in upstream_actors:
            upstream_actor_state = self.get_actor_final_state(upstream_actor)
            # 如果上游算子有至少一个没有结束，继续
            if not upstream_actor_state == actor_constant.ACTOR_STATE_FAILED:
                all_failed = False
                break
        return all_failed

    def check_finished(self, upstream_actors):
        # 是否停止该actor
        finished = True
        for upstream_actor in upstream_actors:
            upstream_actor_state = self.get_actor_final_state(upstream_actor)
            # 如果上游算子有至少一个没有结束，继续
            if not (upstream_actor_state == actor_constant.ACTOR_STATE_SUCCESS
                    or upstream_actor_state == actor_constant.ACTOR_STATE_FAILED
                    or upstream_actor_state == actor_constant.ACTOR_STATE_CANCELLED):
                finished = False
                break
        return finished

    def loop_input_port(self):
        print("actor_process_1>>>>>>>>>>>>>>>>>>>>>")
        if isinstance(self.actor, SourceActor):
            print("actor_process_2>>>>>>>>>>>>>>>>>>>>>")
            for item in self.actor.__iter__():
                # self.actor_running()
                print("actor_process_3>>>>>>>>>>>>>>>>>>>>>")
                self.actor.emit(item)
        else:
            print("actor_process_4>>>>>>>>>>>>>>>>>>>>>")
            stream_names_input_map = {}
            upstream_actors = []
            for input_port in self.actor.get_input_ports():
                stream_names_input_map[input_port.channel] = input_port
                upstream_actors.append(input_port.upstream_actor)
            print("actor_process_5>>>>>>>>>>>>>>>>>>>>>")
            consumer_id = generate()
            group_name = self.current_actor_name
            print("actor_process_6>>>>>>>>>>>>>>>>>>>>>")
            while True:
                consumer = RedisConsumer(self.redis_client, group_name, stream_names_input_map.keys())
                msgs = consumer.consume(consumer_id, 1)
                # 如果消息为空，判断上游所有算子状态是否结束
                if len(msgs) <= 0:
                    if self.check_failed(upstream_actors):
                        # self.state_manager.update_actor_state(self.current_actor_name, self.parallel_index,
                        #                                       actor_constant.ACTOR_STATE_FAILED)
                        raise Exception("all upstream job failed!")
                    if self.check_finished(upstream_actors):
                        # self.state_manager.update_actor_state(self.current_actor_name, self.parallel_index,
                        #                                       actor_constant.ACTOR_STATE_SUCCESS)
                        break
                print("actor_process_7>>>>>>>>>>>>>>>>>>>>>")
                # self.actor_running()
                # msgs消息格式
                # [[b'Source&success', [(b'1652346017746-2', {b'': b'{"payload": "C1(=N/NC(COC2C(Cl)=CC(=CC=2Cl)Cl)=O)\\\\C2C=C(Br)C=C(C)C=2N(C)C\\\\1=O\\tMCULE-8250840838\\n", "flag": "0", "type": "TextOutputPort"}'})]]]
                for msg in msgs:
                    print("actor_process_8>>>>>>>>>>>>>>>>>>>>>")
                    # 解析stream_name
                    stream_name = msg[0].decode()
                    msg_items = msg[1]
                    for msg_item in msg_items:
                        print("actor_process_9>>>>>>>>>>>>>>>>>>>>>")
                        # 解析消息ID
                        msg_id = msg_item[0]
                        # 解析消息体
                        msg_body = msg_item[1][b'']
                        # 解析消息体json格式
                        msg_object = serialize_inner.decode(msg_body)

                        # msg_object = json.loads(msg_body)
                        consumer.ack(stream_name, msg_id)
                        input_port = stream_names_input_map[stream_name]
                        print("actor_process_10>>>>>>>>>>>>>>>>>>>>>")
                        # 获取消息payload
                        content = msg_object.get_payload()
                        if isinstance(self.actor, SinkActor):
                            print("actor_process_11>>>>>>>>>>>>>>>>>>>>>")
                            print('-----sink算子')
                            self.actor.write(content, input_port)
                        elif isinstance(self.actor, ComputeActor) or isinstance(self.actor, ParallelComputeActor):
                            print("actor_process_12>>>>>>>>>>>>>>>>>>>>>")
                            print('----计算算子')
                            self.actor.process(content, input_port)
                        else:
                            pass


    '''
    处理SourceActor
    '''
    def process_actor(self):
        self.actor.begin()
        self.loop_input_port()
        self.actor.end()

    '''
    更新actor的状态为ready
    '''
    def actor_ready(self) -> None:
        # 调用flow_namager接口修改actor的状态为Ready
        self.state_manager.update_actor_state(self.current_actor_name, self.parallel_index, actor_constant.ACTOR_STATE_READY)
        self.current_actor_state = actor_constant.ACTOR_STATE_READY


    '''
    更新actor的状态为stoppable
    '''
    def actor_stoppable(self) -> None:
        # 调用flow_namager接口修改actor的状态为Ready
        self.state_manager.update_actor_state(self.current_actor_name, self.parallel_index,
                                              actor_constant.ACTOR_STATE_STOPPABLE)
        self.current_actor_state = actor_constant.ACTOR_STATE_STOPPABLE


    '''
    更新actor的状态为running
    '''
    def actor_running(self) -> None:
        if self.current_actor_state == actor_constant.ACTOR_STATE_READY:
            # 调用flow_namager接口修改actor的状态为running
            self.state_manager.update_actor_state(self.current_actor_name,
                                                  self.parallel_index, actor_constant.ACTOR_STATE_RUNNING)
            self.current_actor_state = actor_constant.ACTOR_STATE_RUNNING



    '''
    查询actor的运行状态
    '''
    def get_actor_final_state(self, actor_name: str) -> str:
        # 查询actor的状态
        state = self.state_manager.get_actor_final_state(actor_name)
        return state


    '''
    获取actor的input_port
    '''
    def get_actor_input_ports(self, actor_desc: dict) -> list:
        input_ports_json = dict_utils.get_property_value(actor_desc, 'input_ports', [])
        input_ports = []
        for input_port_json in input_ports_json:
            # port的类型
            port_class_name = input_port_json.get('class')
            # port的名称
            port_name = input_port_json.get('name')
            # port依赖的上游actor
            # TODO 只取第一个
            connect = input_port_json['connect'][0]
            upstream_actor_name = connect['actor']
            upstream_actor_port = connect['port']
            module = str(config.INPUT_PORT_PATH)
            input_port_module = importlib.import_module(module)
            port_class = getattr(input_port_module, port_class_name)
            input_port = port_class(port_name, self.actor)
            input_port.connect(upstream_actor_name, upstream_actor_port)
            # 把用户定义的port空对象用真实的对象覆盖
            setattr(self.actor, port_name, input_port)
            input_ports.append(input_port)
        return input_ports


    '''
    获取actor的output_port
    '''
    def get_actor_output_ports(self, actor_desc: dict) -> list:
        output_ports_json = dict_utils.get_property_value(actor_desc, 'output_ports', [])
        output_ports = []
        producer = RedisProducer(redis_client=self.redis_client, flow_depth=self.flow_depth,
                                 actor_level=self.actor_level)
        for output_port_json in output_ports_json:
            # port的类型
            port_class_name = output_port_json.get('class')
            # port的名称
            port_name = output_port_json.get('name')
            # port依赖的上游actor
            module = str(config.OUTPUT_PORT_PATH)
            output_port_module = importlib.import_module(module)
            port_class = getattr(output_port_module, port_class_name)
            output_port = port_class(producer=producer, name=port_name, actor_name=self.current_actor_name)
            output_ports.append(output_port)
            # 把用户定义的port空对象用真实的对象覆盖
            setattr(self.actor, port_name, output_port)
        return output_ports


    '''
    获取actor的params
    '''
    # system_parameters = ["core_num", "partition", "parallel_num", "ntask"]
    def get_actor_params(self, actor_desc: json) -> Args:
        params_json = dict_utils.get_property_value(actor_desc, 'parameters', [])
        args = Args()
        for param in params_json:
            # type
            param_type = param.get('type')
            # param的变量名
            param_variable = param.get('variable')
            # param显示的名称
            param_name = param.get('name')
            # param显示的值
            param_value = param.get('value')
            # param显示的描述
            param_description = param.get('description')
            # port依赖的上游actor
            module = str(config.PARAM_PATH)
            param_module = importlib.import_module(module)
            param_class = getattr(param_module, param_type)
            param = param_class(name=param_name)
            setattr(args, param_variable, param_value)
            setattr(args, param_variable+"_object", param)
        return args

    def run(self):
        self.actor_id = os.getenv("actor_id")
        self.flow_depth = int(os.getenv("flow_depth"))
        self.actor_level = int(os.getenv("actor_level"))
        self.parallel_index = int(os.getenv("parallel_index"))

        redis_host = os.getenv("redis_host")
        pool = ConnectionPool(max_connections=1, host=redis_host, port=6379, password='123456')
        self.redis_client = StrictRedis(connection_pool=pool)
        self.state_manager = FlowStateUtils(self.redis_client)

        # 获取actor 描述
        actor_desc = os.getenv("actor_desc")
        # base64解码参数
        actor_desc_arg = base64_utils.decode(actor_desc)
        actor_json = json.loads(actor_desc_arg)
        self.current_actor_name = actor_json.get('name')

        # set actor 变量参数
        params = self.get_actor_params(actor_json)
        print("actor_json>>>>"+json.dumps(actor_json))
        print("params>>>>"+str(params))
        self.actor.args = params
        # TODO get_set_param,get_set_runtime_param
        input_ports = self.get_actor_input_ports(actor_json)
        print("input_ports>>>>" + str(input_ports))
        output_ports = self.get_actor_output_ports(actor_json)
        print("output_ports>>>>" + str(output_ports))
        self.actor.set_input_ports(input_ports)
        self.actor.set_output_ports(output_ports)
        # 设置actor状态为已开始
        # self.actor_ready()
        print("process_source_actor>>>>>start")
        self.process_actor()
        print("process_source_actor>>>>>end")

