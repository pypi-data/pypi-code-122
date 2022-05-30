# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorflow/core/framework/resource_handle.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from pythie_serving.tensorflow_proto.tensorflow.core.framework import tensor_shape_pb2 as tensorflow_dot_core_dot_framework_dot_tensor__shape__pb2
from pythie_serving.tensorflow_proto.tensorflow.core.framework import types_pb2 as tensorflow_dot_core_dot_framework_dot_types__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='tensorflow/core/framework/resource_handle.proto',
  package='tensorflow',
  syntax='proto3',
  serialized_options=b'\n\030org.tensorflow.frameworkB\016ResourceHandleP\001ZVgithub.com/tensorflow/tensorflow/tensorflow/go/core/framework/resource_handle_go_proto\370\001\001',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n/tensorflow/core/framework/resource_handle.proto\x12\ntensorflow\x1a,tensorflow/core/framework/tensor_shape.proto\x1a%tensorflow/core/framework/types.proto\"\xa5\x02\n\x13ResourceHandleProto\x12\x0e\n\x06\x64\x65vice\x18\x01 \x01(\t\x12\x11\n\tcontainer\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x11\n\thash_code\x18\x04 \x01(\x04\x12\x17\n\x0fmaybe_type_name\x18\x05 \x01(\t\x12H\n\x11\x64types_and_shapes\x18\x06 \x03(\x0b\x32-.tensorflow.ResourceHandleProto.DtypeAndShape\x1a\x61\n\rDtypeAndShape\x12#\n\x05\x64type\x18\x01 \x01(\x0e\x32\x14.tensorflow.DataType\x12+\n\x05shape\x18\x02 \x01(\x0b\x32\x1c.tensorflow.TensorShapeProtoJ\x04\x08\x07\x10\x08\x42\x87\x01\n\x18org.tensorflow.frameworkB\x0eResourceHandleP\x01ZVgithub.com/tensorflow/tensorflow/tensorflow/go/core/framework/resource_handle_go_proto\xf8\x01\x01\x62\x06proto3'
  ,
  dependencies=[tensorflow_dot_core_dot_framework_dot_tensor__shape__pb2.DESCRIPTOR,tensorflow_dot_core_dot_framework_dot_types__pb2.DESCRIPTOR,])




_RESOURCEHANDLEPROTO_DTYPEANDSHAPE = _descriptor.Descriptor(
  name='DtypeAndShape',
  full_name='tensorflow.ResourceHandleProto.DtypeAndShape',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='dtype', full_name='tensorflow.ResourceHandleProto.DtypeAndShape.dtype', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='shape', full_name='tensorflow.ResourceHandleProto.DtypeAndShape.shape', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=339,
  serialized_end=436,
)

_RESOURCEHANDLEPROTO = _descriptor.Descriptor(
  name='ResourceHandleProto',
  full_name='tensorflow.ResourceHandleProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='device', full_name='tensorflow.ResourceHandleProto.device', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='container', full_name='tensorflow.ResourceHandleProto.container', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='tensorflow.ResourceHandleProto.name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='hash_code', full_name='tensorflow.ResourceHandleProto.hash_code', index=3,
      number=4, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='maybe_type_name', full_name='tensorflow.ResourceHandleProto.maybe_type_name', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dtypes_and_shapes', full_name='tensorflow.ResourceHandleProto.dtypes_and_shapes', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_RESOURCEHANDLEPROTO_DTYPEANDSHAPE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=149,
  serialized_end=442,
)

_RESOURCEHANDLEPROTO_DTYPEANDSHAPE.fields_by_name['dtype'].enum_type = tensorflow_dot_core_dot_framework_dot_types__pb2._DATATYPE
_RESOURCEHANDLEPROTO_DTYPEANDSHAPE.fields_by_name['shape'].message_type = tensorflow_dot_core_dot_framework_dot_tensor__shape__pb2._TENSORSHAPEPROTO
_RESOURCEHANDLEPROTO_DTYPEANDSHAPE.containing_type = _RESOURCEHANDLEPROTO
_RESOURCEHANDLEPROTO.fields_by_name['dtypes_and_shapes'].message_type = _RESOURCEHANDLEPROTO_DTYPEANDSHAPE
DESCRIPTOR.message_types_by_name['ResourceHandleProto'] = _RESOURCEHANDLEPROTO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ResourceHandleProto = _reflection.GeneratedProtocolMessageType('ResourceHandleProto', (_message.Message,), {

  'DtypeAndShape' : _reflection.GeneratedProtocolMessageType('DtypeAndShape', (_message.Message,), {
    'DESCRIPTOR' : _RESOURCEHANDLEPROTO_DTYPEANDSHAPE,
    '__module__' : 'tensorflow.core.framework.resource_handle_pb2'
    # @@protoc_insertion_point(class_scope:tensorflow.ResourceHandleProto.DtypeAndShape)
    })
  ,
  'DESCRIPTOR' : _RESOURCEHANDLEPROTO,
  '__module__' : 'tensorflow.core.framework.resource_handle_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.ResourceHandleProto)
  })
_sym_db.RegisterMessage(ResourceHandleProto)
_sym_db.RegisterMessage(ResourceHandleProto.DtypeAndShape)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
