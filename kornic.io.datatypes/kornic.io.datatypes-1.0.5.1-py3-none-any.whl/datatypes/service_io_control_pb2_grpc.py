# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import edge_core.datatypes.io_common_pb2 as io__common__pb2
import edge_core.datatypes.service_io_control_pb2 as service__io__control__pb2


class IoControlServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SingleIoControl = channel.unary_unary(
                '/io.v2.IoControlService/SingleIoControl',
                request_serializer=service__io__control__pb2.IoControlRequest.SerializeToString,
                response_deserializer=service__io__control__pb2.IoControlResponse.FromString,
                )
        self.GetIoList = channel.unary_unary(
                '/io.v2.IoControlService/GetIoList',
                request_serializer=io__common__pb2.Empty.SerializeToString,
                response_deserializer=service__io__control__pb2.IoListResponse.FromString,
                )


class IoControlServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SingleIoControl(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetIoList(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_IoControlServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SingleIoControl': grpc.unary_unary_rpc_method_handler(
                    servicer.SingleIoControl,
                    request_deserializer=service__io__control__pb2.IoControlRequest.FromString,
                    response_serializer=service__io__control__pb2.IoControlResponse.SerializeToString,
            ),
            'GetIoList': grpc.unary_unary_rpc_method_handler(
                    servicer.GetIoList,
                    request_deserializer=io__common__pb2.Empty.FromString,
                    response_serializer=service__io__control__pb2.IoListResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'io.v2.IoControlService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class IoControlService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SingleIoControl(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/io.v2.IoControlService/SingleIoControl',
            service__io__control__pb2.IoControlRequest.SerializeToString,
            service__io__control__pb2.IoControlResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetIoList(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/io.v2.IoControlService/GetIoList',
            io__common__pb2.Empty.SerializeToString,
            service__io__control__pb2.IoListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
