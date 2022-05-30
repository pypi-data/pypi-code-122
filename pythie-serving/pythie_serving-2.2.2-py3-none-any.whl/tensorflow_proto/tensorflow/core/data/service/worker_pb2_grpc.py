# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from pythie_serving.tensorflow_proto.tensorflow.core.data.service import worker_pb2 as tensorflow_dot_core_dot_data_dot_service_dot_worker__pb2


class WorkerServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ProcessTask = channel.unary_unary(
                '/tensorflow.data.WorkerService/ProcessTask',
                request_serializer=tensorflow_dot_core_dot_data_dot_service_dot_worker__pb2.ProcessTaskRequest.SerializeToString,
                response_deserializer=tensorflow_dot_core_dot_data_dot_service_dot_worker__pb2.ProcessTaskResponse.FromString,
                )
        self.GetElement = channel.unary_unary(
                '/tensorflow.data.WorkerService/GetElement',
                request_serializer=tensorflow_dot_core_dot_data_dot_service_dot_worker__pb2.GetElementRequest.SerializeToString,
                response_deserializer=tensorflow_dot_core_dot_data_dot_service_dot_worker__pb2.GetElementResponse.FromString,
                )


class WorkerServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ProcessTask(self, request, context):
        """Processes an task for a dataset, making elements available to clients.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetElement(self, request, context):
        """Gets the next dataset element.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WorkerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ProcessTask': grpc.unary_unary_rpc_method_handler(
                    servicer.ProcessTask,
                    request_deserializer=tensorflow_dot_core_dot_data_dot_service_dot_worker__pb2.ProcessTaskRequest.FromString,
                    response_serializer=tensorflow_dot_core_dot_data_dot_service_dot_worker__pb2.ProcessTaskResponse.SerializeToString,
            ),
            'GetElement': grpc.unary_unary_rpc_method_handler(
                    servicer.GetElement,
                    request_deserializer=tensorflow_dot_core_dot_data_dot_service_dot_worker__pb2.GetElementRequest.FromString,
                    response_serializer=tensorflow_dot_core_dot_data_dot_service_dot_worker__pb2.GetElementResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'tensorflow.data.WorkerService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class WorkerService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ProcessTask(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tensorflow.data.WorkerService/ProcessTask',
            tensorflow_dot_core_dot_data_dot_service_dot_worker__pb2.ProcessTaskRequest.SerializeToString,
            tensorflow_dot_core_dot_data_dot_service_dot_worker__pb2.ProcessTaskResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetElement(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/tensorflow.data.WorkerService/GetElement',
            tensorflow_dot_core_dot_data_dot_service_dot_worker__pb2.GetElementRequest.SerializeToString,
            tensorflow_dot_core_dot_data_dot_service_dot_worker__pb2.GetElementResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
