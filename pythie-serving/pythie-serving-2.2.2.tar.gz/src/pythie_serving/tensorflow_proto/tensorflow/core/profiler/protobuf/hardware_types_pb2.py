# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorflow/core/profiler/protobuf/hardware_types.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='tensorflow/core/profiler/protobuf/hardware_types.proto',
  package='tensorflow.profiler',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n6tensorflow/core/profiler/protobuf/hardware_types.proto\x12\x13tensorflow.profiler\"5\n\x15\x43udaComputeCapability\x12\r\n\x05major\x18\x01 \x01(\r\x12\r\n\x05minor\x18\x02 \x01(\r\"\xc2\x01\n\x12\x44\x65viceCapabilities\x12\x19\n\x11\x63lock_rate_in_ghz\x18\x01 \x01(\x01\x12\x11\n\tnum_cores\x18\x02 \x01(\r\x12\x1c\n\x14memory_size_in_bytes\x18\x03 \x01(\x04\x12\x18\n\x10memory_bandwidth\x18\x04 \x01(\x04\x12\x46\n\x12\x63ompute_capability\x18\x05 \x01(\x0b\x32*.tensorflow.profiler.CudaComputeCapability*D\n\x0cHardwareType\x12\x14\n\x10UNKNOWN_HARDWARE\x10\x00\x12\x0c\n\x08\x43PU_ONLY\x10\x01\x12\x07\n\x03GPU\x10\x02\x12\x07\n\x03TPU\x10\x03\x62\x06proto3'
)

_HARDWARETYPE = _descriptor.EnumDescriptor(
  name='HardwareType',
  full_name='tensorflow.profiler.HardwareType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN_HARDWARE', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='CPU_ONLY', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='GPU', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TPU', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=331,
  serialized_end=399,
)
_sym_db.RegisterEnumDescriptor(_HARDWARETYPE)

HardwareType = enum_type_wrapper.EnumTypeWrapper(_HARDWARETYPE)
UNKNOWN_HARDWARE = 0
CPU_ONLY = 1
GPU = 2
TPU = 3



_CUDACOMPUTECAPABILITY = _descriptor.Descriptor(
  name='CudaComputeCapability',
  full_name='tensorflow.profiler.CudaComputeCapability',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='major', full_name='tensorflow.profiler.CudaComputeCapability.major', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='minor', full_name='tensorflow.profiler.CudaComputeCapability.minor', index=1,
      number=2, type=13, cpp_type=3, label=1,
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
  serialized_start=79,
  serialized_end=132,
)


_DEVICECAPABILITIES = _descriptor.Descriptor(
  name='DeviceCapabilities',
  full_name='tensorflow.profiler.DeviceCapabilities',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='clock_rate_in_ghz', full_name='tensorflow.profiler.DeviceCapabilities.clock_rate_in_ghz', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='num_cores', full_name='tensorflow.profiler.DeviceCapabilities.num_cores', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='memory_size_in_bytes', full_name='tensorflow.profiler.DeviceCapabilities.memory_size_in_bytes', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='memory_bandwidth', full_name='tensorflow.profiler.DeviceCapabilities.memory_bandwidth', index=3,
      number=4, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='compute_capability', full_name='tensorflow.profiler.DeviceCapabilities.compute_capability', index=4,
      number=5, type=11, cpp_type=10, label=1,
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
  serialized_start=135,
  serialized_end=329,
)

_DEVICECAPABILITIES.fields_by_name['compute_capability'].message_type = _CUDACOMPUTECAPABILITY
DESCRIPTOR.message_types_by_name['CudaComputeCapability'] = _CUDACOMPUTECAPABILITY
DESCRIPTOR.message_types_by_name['DeviceCapabilities'] = _DEVICECAPABILITIES
DESCRIPTOR.enum_types_by_name['HardwareType'] = _HARDWARETYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CudaComputeCapability = _reflection.GeneratedProtocolMessageType('CudaComputeCapability', (_message.Message,), {
  'DESCRIPTOR' : _CUDACOMPUTECAPABILITY,
  '__module__' : 'tensorflow.core.profiler.protobuf.hardware_types_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.profiler.CudaComputeCapability)
  })
_sym_db.RegisterMessage(CudaComputeCapability)

DeviceCapabilities = _reflection.GeneratedProtocolMessageType('DeviceCapabilities', (_message.Message,), {
  'DESCRIPTOR' : _DEVICECAPABILITIES,
  '__module__' : 'tensorflow.core.profiler.protobuf.hardware_types_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.profiler.DeviceCapabilities)
  })
_sym_db.RegisterMessage(DeviceCapabilities)


# @@protoc_insertion_point(module_scope)
