# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sinker_batch_payload.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import edge_core.datatypes.data_source_property_pb2 as data__source__property__pb2
try:
  io__property__pb2 = data__source__property__pb2.io__property__pb2
except AttributeError:
  io__property__pb2 = data__source__property__pb2.io_property_pb2
import edge_core.datatypes.io_property_pb2 as io__property__pb2
import edge_core.datatypes.sinker_io_payload_pb2 as sinker__io__payload__pb2
try:
  io__common__pb2 = sinker__io__payload__pb2.io__common__pb2
except AttributeError:
  io__common__pb2 = sinker__io__payload__pb2.io_common_pb2
try:
  io__property__pb2 = sinker__io__payload__pb2.io__property__pb2
except AttributeError:
  io__property__pb2 = sinker__io__payload__pb2.io_property_pb2

from edge_core.datatypes.data_source_property_pb2 import *
from edge_core.datatypes.io_property_pb2 import *
from edge_core.datatypes.sinker_io_payload_pb2 import *

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1asinker_batch_payload.proto\x12\x05io.v2\x1a\x1a\x64\x61ta_source_property.proto\x1a\x11io_property.proto\x1a\x17sinker_io_payload.proto\"\xa8\x01\n\x08NestedIo\x12&\n\x0bio_property\x18\x01 \x01(\x0b\x32\x11.io.v2.IoProperty\x12&\n\x0bmethod_type\x18\x02 \x01(\x0e\x32\x11.io.v2.MethodType\x12!\n\tset_value\x18\x03 \x01(\x0b\x32\x0e.io.v2.IoValue\x12)\n\tget_value\x18\x04 \x01(\x0b\x32\x16.io.v2.ResponseDataset\"\x90\x01\n\x14\x42\x61tchRequestToSinker\x12$\n\x06header\x18\x01 \x01(\x0b\x32\x14.io.v2.MessageHeader\x12.\n\x0b\x64\x61ta_source\x18\x02 \x01(\x0b\x32\x19.io.v2.DataSourceProperty\x12\"\n\tnested_io\x18\x03 \x03(\x0b\x32\x0f.io.v2.NestedIo\"\xba\x01\n\x17\x42\x61tchResponseFromSinker\x12$\n\x06header\x18\x01 \x01(\x0b\x32\x14.io.v2.MessageHeader\x12.\n\x0b\x64\x61ta_source\x18\x02 \x01(\x0b\x32\x19.io.v2.DataSourceProperty\x12\"\n\tnested_io\x18\x03 \x03(\x0b\x32\x0f.io.v2.NestedIo\x12%\n\x06result\x18\x04 \x01(\x0b\x32\x15.io.v2.ResponseResultP\x00P\x01P\x02\x62\x06proto3')



_NESTEDIO = DESCRIPTOR.message_types_by_name['NestedIo']
_BATCHREQUESTTOSINKER = DESCRIPTOR.message_types_by_name['BatchRequestToSinker']
_BATCHRESPONSEFROMSINKER = DESCRIPTOR.message_types_by_name['BatchResponseFromSinker']
NestedIo = _reflection.GeneratedProtocolMessageType('NestedIo', (_message.Message,), {
  'DESCRIPTOR' : _NESTEDIO,
  '__module__' : 'sinker_batch_payload_pb2'
  # @@protoc_insertion_point(class_scope:io.v2.NestedIo)
  })
_sym_db.RegisterMessage(NestedIo)

BatchRequestToSinker = _reflection.GeneratedProtocolMessageType('BatchRequestToSinker', (_message.Message,), {
  'DESCRIPTOR' : _BATCHREQUESTTOSINKER,
  '__module__' : 'sinker_batch_payload_pb2'
  # @@protoc_insertion_point(class_scope:io.v2.BatchRequestToSinker)
  })
_sym_db.RegisterMessage(BatchRequestToSinker)

BatchResponseFromSinker = _reflection.GeneratedProtocolMessageType('BatchResponseFromSinker', (_message.Message,), {
  'DESCRIPTOR' : _BATCHRESPONSEFROMSINKER,
  '__module__' : 'sinker_batch_payload_pb2'
  # @@protoc_insertion_point(class_scope:io.v2.BatchResponseFromSinker)
  })
_sym_db.RegisterMessage(BatchResponseFromSinker)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _NESTEDIO._serialized_start=110
  _NESTEDIO._serialized_end=278
  _BATCHREQUESTTOSINKER._serialized_start=281
  _BATCHREQUESTTOSINKER._serialized_end=425
  _BATCHRESPONSEFROMSINKER._serialized_start=428
  _BATCHRESPONSEFROMSINKER._serialized_end=614
# @@protoc_insertion_point(module_scope)
