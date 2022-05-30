# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorflow/core/framework/graph_transfer_info.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from pythie_serving.tensorflow_proto.tensorflow.core.framework import types_pb2 as tensorflow_dot_core_dot_framework_dot_types__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='tensorflow/core/framework/graph_transfer_info.proto',
  package='tensorflow',
  syntax='proto3',
  serialized_options=b'\n\030org.tensorflow.frameworkB\026GraphTransferInfoProtoP\001ZZgithub.com/tensorflow/tensorflow/tensorflow/go/core/framework/graph_transfer_info_go_proto\370\001\001',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n3tensorflow/core/framework/graph_transfer_info.proto\x12\ntensorflow\x1a%tensorflow/core/framework/types.proto\">\n\x16GraphTransferNodeInput\x12\x0f\n\x07node_id\x18\x01 \x01(\x05\x12\x13\n\x0boutput_port\x18\x02 \x01(\x05\"\x9b\x01\n\x15GraphTransferNodeInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07node_id\x18\x02 \x01(\x05\x12\x11\n\ttype_name\x18\x03 \x01(\t\x12\x11\n\tsoc_op_id\x18\x04 \x01(\x05\x12\x12\n\npadding_id\x18\x05 \x01(\x05\x12\x13\n\x0binput_count\x18\x06 \x01(\x05\x12\x14\n\x0coutput_count\x18\x07 \x01(\x05\"}\n\x1aGraphTransferConstNodeInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07node_id\x18\x02 \x01(\x05\x12\r\n\x05shape\x18\x03 \x03(\x03\x12\x0c\n\x04\x64\x61ta\x18\x04 \x01(\x0c\x12#\n\x05\x64type\x18\x05 \x01(\x0e\x32\x14.tensorflow.DataType\"e\n\x1aGraphTransferNodeInputInfo\x12\x0f\n\x07node_id\x18\x01 \x01(\x05\x12\x36\n\nnode_input\x18\x02 \x03(\x0b\x32\".tensorflow.GraphTransferNodeInput\"E\n\x1bGraphTransferNodeOutputInfo\x12\x0f\n\x07node_id\x18\x01 \x01(\x05\x12\x15\n\rmax_byte_size\x18\x02 \x03(\x05\"c\n\x1fGraphTransferGraphInputNodeInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05shape\x18\x02 \x03(\x03\x12#\n\x05\x64type\x18\x03 \x01(\x0e\x32\x14.tensorflow.DataType\"d\n GraphTransferGraphOutputNodeInfo\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05shape\x18\x02 \x03(\x03\x12#\n\x05\x64type\x18\x03 \x01(\x0e\x32\x14.tensorflow.DataType\"\x8d\x04\n\x11GraphTransferInfo\x12\x34\n\tnode_info\x18\x01 \x03(\x0b\x32!.tensorflow.GraphTransferNodeInfo\x12?\n\x0f\x63onst_node_info\x18\x02 \x03(\x0b\x32&.tensorflow.GraphTransferConstNodeInfo\x12?\n\x0fnode_input_info\x18\x03 \x03(\x0b\x32&.tensorflow.GraphTransferNodeInputInfo\x12\x41\n\x10node_output_info\x18\x04 \x03(\x0b\x32\'.tensorflow.GraphTransferNodeOutputInfo\x12J\n\x15graph_input_node_info\x18\x05 \x03(\x0b\x32+.tensorflow.GraphTransferGraphInputNodeInfo\x12L\n\x16graph_output_node_info\x18\x06 \x03(\x0b\x32,.tensorflow.GraphTransferGraphOutputNodeInfo\x12>\n\x0b\x64\x65stination\x18\x07 \x01(\x0e\x32).tensorflow.GraphTransferInfo.Destination\"#\n\x0b\x44\x65stination\x12\x07\n\x03NOP\x10\x00\x12\x0b\n\x07HEXAGON\x10\x01\x42\x93\x01\n\x18org.tensorflow.frameworkB\x16GraphTransferInfoProtoP\x01ZZgithub.com/tensorflow/tensorflow/tensorflow/go/core/framework/graph_transfer_info_go_proto\xf8\x01\x01\x62\x06proto3'
  ,
  dependencies=[tensorflow_dot_core_dot_framework_dot_types__pb2.DESCRIPTOR,])



_GRAPHTRANSFERINFO_DESTINATION = _descriptor.EnumDescriptor(
  name='Destination',
  full_name='tensorflow.GraphTransferInfo.Destination',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NOP', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='HEXAGON', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1323,
  serialized_end=1358,
)
_sym_db.RegisterEnumDescriptor(_GRAPHTRANSFERINFO_DESTINATION)


_GRAPHTRANSFERNODEINPUT = _descriptor.Descriptor(
  name='GraphTransferNodeInput',
  full_name='tensorflow.GraphTransferNodeInput',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='node_id', full_name='tensorflow.GraphTransferNodeInput.node_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='output_port', full_name='tensorflow.GraphTransferNodeInput.output_port', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=106,
  serialized_end=168,
)


_GRAPHTRANSFERNODEINFO = _descriptor.Descriptor(
  name='GraphTransferNodeInfo',
  full_name='tensorflow.GraphTransferNodeInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='tensorflow.GraphTransferNodeInfo.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='node_id', full_name='tensorflow.GraphTransferNodeInfo.node_id', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='type_name', full_name='tensorflow.GraphTransferNodeInfo.type_name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='soc_op_id', full_name='tensorflow.GraphTransferNodeInfo.soc_op_id', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='padding_id', full_name='tensorflow.GraphTransferNodeInfo.padding_id', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='input_count', full_name='tensorflow.GraphTransferNodeInfo.input_count', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='output_count', full_name='tensorflow.GraphTransferNodeInfo.output_count', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=171,
  serialized_end=326,
)


_GRAPHTRANSFERCONSTNODEINFO = _descriptor.Descriptor(
  name='GraphTransferConstNodeInfo',
  full_name='tensorflow.GraphTransferConstNodeInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='tensorflow.GraphTransferConstNodeInfo.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='node_id', full_name='tensorflow.GraphTransferConstNodeInfo.node_id', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='shape', full_name='tensorflow.GraphTransferConstNodeInfo.shape', index=2,
      number=3, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='data', full_name='tensorflow.GraphTransferConstNodeInfo.data', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dtype', full_name='tensorflow.GraphTransferConstNodeInfo.dtype', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=328,
  serialized_end=453,
)


_GRAPHTRANSFERNODEINPUTINFO = _descriptor.Descriptor(
  name='GraphTransferNodeInputInfo',
  full_name='tensorflow.GraphTransferNodeInputInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='node_id', full_name='tensorflow.GraphTransferNodeInputInfo.node_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='node_input', full_name='tensorflow.GraphTransferNodeInputInfo.node_input', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=455,
  serialized_end=556,
)


_GRAPHTRANSFERNODEOUTPUTINFO = _descriptor.Descriptor(
  name='GraphTransferNodeOutputInfo',
  full_name='tensorflow.GraphTransferNodeOutputInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='node_id', full_name='tensorflow.GraphTransferNodeOutputInfo.node_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='max_byte_size', full_name='tensorflow.GraphTransferNodeOutputInfo.max_byte_size', index=1,
      number=2, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=558,
  serialized_end=627,
)


_GRAPHTRANSFERGRAPHINPUTNODEINFO = _descriptor.Descriptor(
  name='GraphTransferGraphInputNodeInfo',
  full_name='tensorflow.GraphTransferGraphInputNodeInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='tensorflow.GraphTransferGraphInputNodeInfo.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='shape', full_name='tensorflow.GraphTransferGraphInputNodeInfo.shape', index=1,
      number=2, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dtype', full_name='tensorflow.GraphTransferGraphInputNodeInfo.dtype', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=629,
  serialized_end=728,
)


_GRAPHTRANSFERGRAPHOUTPUTNODEINFO = _descriptor.Descriptor(
  name='GraphTransferGraphOutputNodeInfo',
  full_name='tensorflow.GraphTransferGraphOutputNodeInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='tensorflow.GraphTransferGraphOutputNodeInfo.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='shape', full_name='tensorflow.GraphTransferGraphOutputNodeInfo.shape', index=1,
      number=2, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dtype', full_name='tensorflow.GraphTransferGraphOutputNodeInfo.dtype', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=730,
  serialized_end=830,
)


_GRAPHTRANSFERINFO = _descriptor.Descriptor(
  name='GraphTransferInfo',
  full_name='tensorflow.GraphTransferInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='node_info', full_name='tensorflow.GraphTransferInfo.node_info', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='const_node_info', full_name='tensorflow.GraphTransferInfo.const_node_info', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='node_input_info', full_name='tensorflow.GraphTransferInfo.node_input_info', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='node_output_info', full_name='tensorflow.GraphTransferInfo.node_output_info', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='graph_input_node_info', full_name='tensorflow.GraphTransferInfo.graph_input_node_info', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='graph_output_node_info', full_name='tensorflow.GraphTransferInfo.graph_output_node_info', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='destination', full_name='tensorflow.GraphTransferInfo.destination', index=6,
      number=7, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _GRAPHTRANSFERINFO_DESTINATION,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=833,
  serialized_end=1358,
)

_GRAPHTRANSFERCONSTNODEINFO.fields_by_name['dtype'].enum_type = tensorflow_dot_core_dot_framework_dot_types__pb2._DATATYPE
_GRAPHTRANSFERNODEINPUTINFO.fields_by_name['node_input'].message_type = _GRAPHTRANSFERNODEINPUT
_GRAPHTRANSFERGRAPHINPUTNODEINFO.fields_by_name['dtype'].enum_type = tensorflow_dot_core_dot_framework_dot_types__pb2._DATATYPE
_GRAPHTRANSFERGRAPHOUTPUTNODEINFO.fields_by_name['dtype'].enum_type = tensorflow_dot_core_dot_framework_dot_types__pb2._DATATYPE
_GRAPHTRANSFERINFO.fields_by_name['node_info'].message_type = _GRAPHTRANSFERNODEINFO
_GRAPHTRANSFERINFO.fields_by_name['const_node_info'].message_type = _GRAPHTRANSFERCONSTNODEINFO
_GRAPHTRANSFERINFO.fields_by_name['node_input_info'].message_type = _GRAPHTRANSFERNODEINPUTINFO
_GRAPHTRANSFERINFO.fields_by_name['node_output_info'].message_type = _GRAPHTRANSFERNODEOUTPUTINFO
_GRAPHTRANSFERINFO.fields_by_name['graph_input_node_info'].message_type = _GRAPHTRANSFERGRAPHINPUTNODEINFO
_GRAPHTRANSFERINFO.fields_by_name['graph_output_node_info'].message_type = _GRAPHTRANSFERGRAPHOUTPUTNODEINFO
_GRAPHTRANSFERINFO.fields_by_name['destination'].enum_type = _GRAPHTRANSFERINFO_DESTINATION
_GRAPHTRANSFERINFO_DESTINATION.containing_type = _GRAPHTRANSFERINFO
DESCRIPTOR.message_types_by_name['GraphTransferNodeInput'] = _GRAPHTRANSFERNODEINPUT
DESCRIPTOR.message_types_by_name['GraphTransferNodeInfo'] = _GRAPHTRANSFERNODEINFO
DESCRIPTOR.message_types_by_name['GraphTransferConstNodeInfo'] = _GRAPHTRANSFERCONSTNODEINFO
DESCRIPTOR.message_types_by_name['GraphTransferNodeInputInfo'] = _GRAPHTRANSFERNODEINPUTINFO
DESCRIPTOR.message_types_by_name['GraphTransferNodeOutputInfo'] = _GRAPHTRANSFERNODEOUTPUTINFO
DESCRIPTOR.message_types_by_name['GraphTransferGraphInputNodeInfo'] = _GRAPHTRANSFERGRAPHINPUTNODEINFO
DESCRIPTOR.message_types_by_name['GraphTransferGraphOutputNodeInfo'] = _GRAPHTRANSFERGRAPHOUTPUTNODEINFO
DESCRIPTOR.message_types_by_name['GraphTransferInfo'] = _GRAPHTRANSFERINFO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GraphTransferNodeInput = _reflection.GeneratedProtocolMessageType('GraphTransferNodeInput', (_message.Message,), {
  'DESCRIPTOR' : _GRAPHTRANSFERNODEINPUT,
  '__module__' : 'tensorflow.core.framework.graph_transfer_info_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.GraphTransferNodeInput)
  })
_sym_db.RegisterMessage(GraphTransferNodeInput)

GraphTransferNodeInfo = _reflection.GeneratedProtocolMessageType('GraphTransferNodeInfo', (_message.Message,), {
  'DESCRIPTOR' : _GRAPHTRANSFERNODEINFO,
  '__module__' : 'tensorflow.core.framework.graph_transfer_info_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.GraphTransferNodeInfo)
  })
_sym_db.RegisterMessage(GraphTransferNodeInfo)

GraphTransferConstNodeInfo = _reflection.GeneratedProtocolMessageType('GraphTransferConstNodeInfo', (_message.Message,), {
  'DESCRIPTOR' : _GRAPHTRANSFERCONSTNODEINFO,
  '__module__' : 'tensorflow.core.framework.graph_transfer_info_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.GraphTransferConstNodeInfo)
  })
_sym_db.RegisterMessage(GraphTransferConstNodeInfo)

GraphTransferNodeInputInfo = _reflection.GeneratedProtocolMessageType('GraphTransferNodeInputInfo', (_message.Message,), {
  'DESCRIPTOR' : _GRAPHTRANSFERNODEINPUTINFO,
  '__module__' : 'tensorflow.core.framework.graph_transfer_info_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.GraphTransferNodeInputInfo)
  })
_sym_db.RegisterMessage(GraphTransferNodeInputInfo)

GraphTransferNodeOutputInfo = _reflection.GeneratedProtocolMessageType('GraphTransferNodeOutputInfo', (_message.Message,), {
  'DESCRIPTOR' : _GRAPHTRANSFERNODEOUTPUTINFO,
  '__module__' : 'tensorflow.core.framework.graph_transfer_info_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.GraphTransferNodeOutputInfo)
  })
_sym_db.RegisterMessage(GraphTransferNodeOutputInfo)

GraphTransferGraphInputNodeInfo = _reflection.GeneratedProtocolMessageType('GraphTransferGraphInputNodeInfo', (_message.Message,), {
  'DESCRIPTOR' : _GRAPHTRANSFERGRAPHINPUTNODEINFO,
  '__module__' : 'tensorflow.core.framework.graph_transfer_info_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.GraphTransferGraphInputNodeInfo)
  })
_sym_db.RegisterMessage(GraphTransferGraphInputNodeInfo)

GraphTransferGraphOutputNodeInfo = _reflection.GeneratedProtocolMessageType('GraphTransferGraphOutputNodeInfo', (_message.Message,), {
  'DESCRIPTOR' : _GRAPHTRANSFERGRAPHOUTPUTNODEINFO,
  '__module__' : 'tensorflow.core.framework.graph_transfer_info_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.GraphTransferGraphOutputNodeInfo)
  })
_sym_db.RegisterMessage(GraphTransferGraphOutputNodeInfo)

GraphTransferInfo = _reflection.GeneratedProtocolMessageType('GraphTransferInfo', (_message.Message,), {
  'DESCRIPTOR' : _GRAPHTRANSFERINFO,
  '__module__' : 'tensorflow.core.framework.graph_transfer_info_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.GraphTransferInfo)
  })
_sym_db.RegisterMessage(GraphTransferInfo)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
