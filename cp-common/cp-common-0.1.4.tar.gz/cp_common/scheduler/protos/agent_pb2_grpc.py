# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import cp_common.scheduler.protos.agent_pb2 as agent__pb2


class AgentServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Ping = channel.unary_unary(
            "/AgentService/Ping",
            request_serializer=agent__pb2.PingRequest.SerializeToString,
            response_deserializer=agent__pb2.PongResponse.FromString,
        )
        self.HeartBeat = channel.unary_unary(
            "/AgentService/HeartBeat",
            request_serializer=agent__pb2.HeartBeatRequest.SerializeToString,
            response_deserializer=agent__pb2.CurrencyResponse.FromString,
        )
        self.Task = channel.unary_stream(
            "/AgentService/Task",
            request_serializer=agent__pb2.GetTaskRequest.SerializeToString,
            response_deserializer=agent__pb2.GetTaskResponse.FromString,
        )
        self.TaskResult = channel.unary_unary(
            "/AgentService/TaskResult",
            request_serializer=agent__pb2.TaskResultRequest.SerializeToString,
            response_deserializer=agent__pb2.CurrencyResponse.FromString,
        )


class AgentServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Ping(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def HeartBeat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def Task(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def TaskResult(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_AgentServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "Ping": grpc.unary_unary_rpc_method_handler(
            servicer.Ping,
            request_deserializer=agent__pb2.PingRequest.FromString,
            response_serializer=agent__pb2.PongResponse.SerializeToString,
        ),
        "HeartBeat": grpc.unary_unary_rpc_method_handler(
            servicer.HeartBeat,
            request_deserializer=agent__pb2.HeartBeatRequest.FromString,
            response_serializer=agent__pb2.CurrencyResponse.SerializeToString,
        ),
        "Task": grpc.unary_stream_rpc_method_handler(
            servicer.Task,
            request_deserializer=agent__pb2.GetTaskRequest.FromString,
            response_serializer=agent__pb2.GetTaskResponse.SerializeToString,
        ),
        "TaskResult": grpc.unary_unary_rpc_method_handler(
            servicer.TaskResult,
            request_deserializer=agent__pb2.TaskResultRequest.FromString,
            response_serializer=agent__pb2.CurrencyResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "AgentService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class AgentService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Ping(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/AgentService/Ping",
            agent__pb2.PingRequest.SerializeToString,
            agent__pb2.PongResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def HeartBeat(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/AgentService/HeartBeat",
            agent__pb2.HeartBeatRequest.SerializeToString,
            agent__pb2.CurrencyResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def Task(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_stream(
            request,
            target,
            "/AgentService/Task",
            agent__pb2.GetTaskRequest.SerializeToString,
            agent__pb2.GetTaskResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def TaskResult(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/AgentService/TaskResult",
            agent__pb2.TaskResultRequest.SerializeToString,
            agent__pb2.CurrencyResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
