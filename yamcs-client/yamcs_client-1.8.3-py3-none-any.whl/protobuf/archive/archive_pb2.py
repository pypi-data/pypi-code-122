# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yamcs/protobuf/archive/archive.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from yamcs.api import annotations_pb2 as yamcs_dot_api_dot_annotations__pb2
from yamcs.api import httpbody_pb2 as yamcs_dot_api_dot_httpbody__pb2
from yamcs.protobuf.pvalue import pvalue_pb2 as yamcs_dot_protobuf_dot_pvalue_dot_pvalue__pb2
from yamcs.protobuf import yamcs_pb2 as yamcs_dot_protobuf_dot_yamcs__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='yamcs/protobuf/archive/archive.proto',
  package='yamcs.protobuf.archive',
  syntax='proto2',
  serialized_options=_b('\n\022org.yamcs.protobuf'),
  serialized_pb=_b('\n$yamcs/protobuf/archive/archive.proto\x12\x16yamcs.protobuf.archive\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1byamcs/api/annotations.proto\x1a\x18yamcs/api/httpbody.proto\x1a\"yamcs/protobuf/pvalue/pvalue.proto\x1a\x1ayamcs/protobuf/yamcs.proto\"\xb1\x01\n\x1cStreamParameterValuesRequest\x12\x10\n\x08instance\x18\x01 \x01(\t\x12)\n\x05start\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12(\n\x04stop\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12*\n\x03ids\x18\x04 \x03(\x0b\x32\x1d.yamcs.protobuf.NamedObjectId\"#\n\x12ParameterGroupInfo\x12\r\n\x05group\x18\x01 \x03(\t\".\n\x1aListParameterGroupsRequest\x12\x10\n\x08instance\x18\x01 \x01(\t\"\x94\x02\n\x1bListParameterHistoryRequest\x12\x10\n\x08instance\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0b\n\x03pos\x18\x03 \x01(\x03\x12\r\n\x05limit\x18\x04 \x01(\x05\x12\x10\n\x08norepeat\x18\x05 \x01(\x08\x12)\n\x05start\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12(\n\x04stop\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\r\n\x05order\x18\x08 \x01(\t\x12\x12\n\nnorealtime\x18\t \x01(\x08\x12\x11\n\tprocessor\x18\n \x01(\t\x12\x0e\n\x06source\x18\x0b \x01(\t\x12\x0c\n\x04next\x18\x0c \x01(\t\"s\n\x1cListParameterHistoryResponse\x12\x38\n\tparameter\x18\x01 \x03(\x0b\x32%.yamcs.protobuf.pvalue.ParameterValue\x12\x19\n\x11\x63ontinuationToken\x18\x02 \x01(\t\"\xec\x01\n\x1aGetParameterSamplesRequest\x12\x10\n\x08instance\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12)\n\x05start\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12(\n\x04stop\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\r\n\x05\x63ount\x18\x05 \x01(\x05\x12\x12\n\nnorealtime\x18\x06 \x01(\x08\x12\x13\n\x0buseRawValue\x18\t \x01(\x08\x12\x11\n\tprocessor\x18\x07 \x01(\t\x12\x0e\n\x06source\x18\x08 \x01(\t\"\xce\x01\n\x1c\x45xportParameterValuesRequest\x12\x10\n\x08instance\x18\x01 \x01(\t\x12)\n\x05start\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12(\n\x04stop\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x12\n\nparameters\x18\x04 \x03(\t\x12\x11\n\tnamespace\x18\x05 \x01(\t\x12\r\n\x05\x65xtra\x18\x06 \x03(\t\x12\x11\n\tdelimiter\x18\x07 \x01(\t2\x82\x07\n\x10StreamArchiveApi\x12\xa5\x01\n\x13ListParameterGroups\x12\x32.yamcs.protobuf.archive.ListParameterGroupsRequest\x1a*.yamcs.protobuf.archive.ParameterGroupInfo\".\x8a\x92\x03*\n(/api/archive/{instance}/parameter-groups\x12\xba\x01\n\x14ListParameterHistory\x12\x33.yamcs.protobuf.archive.ListParameterHistoryRequest\x1a\x34.yamcs.protobuf.archive.ListParameterHistoryResponse\"7\x8a\x92\x03\x33\n1/api/stream-archive/{instance}/parameters/{name*}\x12\xb4\x01\n\x15StreamParameterValues\x12\x34.yamcs.protobuf.archive.StreamParameterValuesRequest\x1a$.yamcs.protobuf.pvalue.ParameterData\"=\x8a\x92\x03\x39\x1a\x34/api/stream-archive/{instance}:streamParameterValues:\x01*0\x01\x12\xb5\x01\n\x13GetParameterSamples\x12\x32.yamcs.protobuf.archive.GetParameterSamplesRequest\x1a!.yamcs.protobuf.pvalue.TimeSeries\"G\x8a\x92\x03\x43\n9/api/stream-archive/{instance}/parameters/{name*}/samplesR\x06sample\x12\x99\x01\n\x15\x45xportParameterValues\x12\x34.yamcs.protobuf.archive.ExportParameterValuesRequest\x1a\x13.yamcs.api.HttpBody\"3\x8a\x92\x03/\n-/api/archive/{instance}:exportParameterValues0\x01\x42\x14\n\x12org.yamcs.protobuf')
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,yamcs_dot_api_dot_annotations__pb2.DESCRIPTOR,yamcs_dot_api_dot_httpbody__pb2.DESCRIPTOR,yamcs_dot_protobuf_dot_pvalue_dot_pvalue__pb2.DESCRIPTOR,yamcs_dot_protobuf_dot_yamcs__pb2.DESCRIPTOR,])




_STREAMPARAMETERVALUESREQUEST = _descriptor.Descriptor(
  name='StreamParameterValuesRequest',
  full_name='yamcs.protobuf.archive.StreamParameterValuesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='instance', full_name='yamcs.protobuf.archive.StreamParameterValuesRequest.instance', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='start', full_name='yamcs.protobuf.archive.StreamParameterValuesRequest.start', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stop', full_name='yamcs.protobuf.archive.StreamParameterValuesRequest.stop', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ids', full_name='yamcs.protobuf.archive.StreamParameterValuesRequest.ids', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=217,
  serialized_end=394,
)


_PARAMETERGROUPINFO = _descriptor.Descriptor(
  name='ParameterGroupInfo',
  full_name='yamcs.protobuf.archive.ParameterGroupInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='group', full_name='yamcs.protobuf.archive.ParameterGroupInfo.group', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=396,
  serialized_end=431,
)


_LISTPARAMETERGROUPSREQUEST = _descriptor.Descriptor(
  name='ListParameterGroupsRequest',
  full_name='yamcs.protobuf.archive.ListParameterGroupsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='instance', full_name='yamcs.protobuf.archive.ListParameterGroupsRequest.instance', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=433,
  serialized_end=479,
)


_LISTPARAMETERHISTORYREQUEST = _descriptor.Descriptor(
  name='ListParameterHistoryRequest',
  full_name='yamcs.protobuf.archive.ListParameterHistoryRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='instance', full_name='yamcs.protobuf.archive.ListParameterHistoryRequest.instance', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='yamcs.protobuf.archive.ListParameterHistoryRequest.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pos', full_name='yamcs.protobuf.archive.ListParameterHistoryRequest.pos', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='limit', full_name='yamcs.protobuf.archive.ListParameterHistoryRequest.limit', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='norepeat', full_name='yamcs.protobuf.archive.ListParameterHistoryRequest.norepeat', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='start', full_name='yamcs.protobuf.archive.ListParameterHistoryRequest.start', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stop', full_name='yamcs.protobuf.archive.ListParameterHistoryRequest.stop', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='order', full_name='yamcs.protobuf.archive.ListParameterHistoryRequest.order', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='norealtime', full_name='yamcs.protobuf.archive.ListParameterHistoryRequest.norealtime', index=8,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='processor', full_name='yamcs.protobuf.archive.ListParameterHistoryRequest.processor', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='source', full_name='yamcs.protobuf.archive.ListParameterHistoryRequest.source', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='next', full_name='yamcs.protobuf.archive.ListParameterHistoryRequest.next', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=482,
  serialized_end=758,
)


_LISTPARAMETERHISTORYRESPONSE = _descriptor.Descriptor(
  name='ListParameterHistoryResponse',
  full_name='yamcs.protobuf.archive.ListParameterHistoryResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='parameter', full_name='yamcs.protobuf.archive.ListParameterHistoryResponse.parameter', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='continuationToken', full_name='yamcs.protobuf.archive.ListParameterHistoryResponse.continuationToken', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=760,
  serialized_end=875,
)


_GETPARAMETERSAMPLESREQUEST = _descriptor.Descriptor(
  name='GetParameterSamplesRequest',
  full_name='yamcs.protobuf.archive.GetParameterSamplesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='instance', full_name='yamcs.protobuf.archive.GetParameterSamplesRequest.instance', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='yamcs.protobuf.archive.GetParameterSamplesRequest.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='start', full_name='yamcs.protobuf.archive.GetParameterSamplesRequest.start', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stop', full_name='yamcs.protobuf.archive.GetParameterSamplesRequest.stop', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='count', full_name='yamcs.protobuf.archive.GetParameterSamplesRequest.count', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='norealtime', full_name='yamcs.protobuf.archive.GetParameterSamplesRequest.norealtime', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='useRawValue', full_name='yamcs.protobuf.archive.GetParameterSamplesRequest.useRawValue', index=6,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='processor', full_name='yamcs.protobuf.archive.GetParameterSamplesRequest.processor', index=7,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='source', full_name='yamcs.protobuf.archive.GetParameterSamplesRequest.source', index=8,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=878,
  serialized_end=1114,
)


_EXPORTPARAMETERVALUESREQUEST = _descriptor.Descriptor(
  name='ExportParameterValuesRequest',
  full_name='yamcs.protobuf.archive.ExportParameterValuesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='instance', full_name='yamcs.protobuf.archive.ExportParameterValuesRequest.instance', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='start', full_name='yamcs.protobuf.archive.ExportParameterValuesRequest.start', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stop', full_name='yamcs.protobuf.archive.ExportParameterValuesRequest.stop', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parameters', full_name='yamcs.protobuf.archive.ExportParameterValuesRequest.parameters', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='namespace', full_name='yamcs.protobuf.archive.ExportParameterValuesRequest.namespace', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='extra', full_name='yamcs.protobuf.archive.ExportParameterValuesRequest.extra', index=5,
      number=6, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='delimiter', full_name='yamcs.protobuf.archive.ExportParameterValuesRequest.delimiter', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1117,
  serialized_end=1323,
)

_STREAMPARAMETERVALUESREQUEST.fields_by_name['start'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_STREAMPARAMETERVALUESREQUEST.fields_by_name['stop'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_STREAMPARAMETERVALUESREQUEST.fields_by_name['ids'].message_type = yamcs_dot_protobuf_dot_yamcs__pb2._NAMEDOBJECTID
_LISTPARAMETERHISTORYREQUEST.fields_by_name['start'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_LISTPARAMETERHISTORYREQUEST.fields_by_name['stop'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_LISTPARAMETERHISTORYRESPONSE.fields_by_name['parameter'].message_type = yamcs_dot_protobuf_dot_pvalue_dot_pvalue__pb2._PARAMETERVALUE
_GETPARAMETERSAMPLESREQUEST.fields_by_name['start'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_GETPARAMETERSAMPLESREQUEST.fields_by_name['stop'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_EXPORTPARAMETERVALUESREQUEST.fields_by_name['start'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_EXPORTPARAMETERVALUESREQUEST.fields_by_name['stop'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
DESCRIPTOR.message_types_by_name['StreamParameterValuesRequest'] = _STREAMPARAMETERVALUESREQUEST
DESCRIPTOR.message_types_by_name['ParameterGroupInfo'] = _PARAMETERGROUPINFO
DESCRIPTOR.message_types_by_name['ListParameterGroupsRequest'] = _LISTPARAMETERGROUPSREQUEST
DESCRIPTOR.message_types_by_name['ListParameterHistoryRequest'] = _LISTPARAMETERHISTORYREQUEST
DESCRIPTOR.message_types_by_name['ListParameterHistoryResponse'] = _LISTPARAMETERHISTORYRESPONSE
DESCRIPTOR.message_types_by_name['GetParameterSamplesRequest'] = _GETPARAMETERSAMPLESREQUEST
DESCRIPTOR.message_types_by_name['ExportParameterValuesRequest'] = _EXPORTPARAMETERVALUESREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

StreamParameterValuesRequest = _reflection.GeneratedProtocolMessageType('StreamParameterValuesRequest', (_message.Message,), dict(
  DESCRIPTOR = _STREAMPARAMETERVALUESREQUEST,
  __module__ = 'yamcs.protobuf.archive.archive_pb2'
  # @@protoc_insertion_point(class_scope:yamcs.protobuf.archive.StreamParameterValuesRequest)
  ))
_sym_db.RegisterMessage(StreamParameterValuesRequest)

ParameterGroupInfo = _reflection.GeneratedProtocolMessageType('ParameterGroupInfo', (_message.Message,), dict(
  DESCRIPTOR = _PARAMETERGROUPINFO,
  __module__ = 'yamcs.protobuf.archive.archive_pb2'
  # @@protoc_insertion_point(class_scope:yamcs.protobuf.archive.ParameterGroupInfo)
  ))
_sym_db.RegisterMessage(ParameterGroupInfo)

ListParameterGroupsRequest = _reflection.GeneratedProtocolMessageType('ListParameterGroupsRequest', (_message.Message,), dict(
  DESCRIPTOR = _LISTPARAMETERGROUPSREQUEST,
  __module__ = 'yamcs.protobuf.archive.archive_pb2'
  # @@protoc_insertion_point(class_scope:yamcs.protobuf.archive.ListParameterGroupsRequest)
  ))
_sym_db.RegisterMessage(ListParameterGroupsRequest)

ListParameterHistoryRequest = _reflection.GeneratedProtocolMessageType('ListParameterHistoryRequest', (_message.Message,), dict(
  DESCRIPTOR = _LISTPARAMETERHISTORYREQUEST,
  __module__ = 'yamcs.protobuf.archive.archive_pb2'
  # @@protoc_insertion_point(class_scope:yamcs.protobuf.archive.ListParameterHistoryRequest)
  ))
_sym_db.RegisterMessage(ListParameterHistoryRequest)

ListParameterHistoryResponse = _reflection.GeneratedProtocolMessageType('ListParameterHistoryResponse', (_message.Message,), dict(
  DESCRIPTOR = _LISTPARAMETERHISTORYRESPONSE,
  __module__ = 'yamcs.protobuf.archive.archive_pb2'
  # @@protoc_insertion_point(class_scope:yamcs.protobuf.archive.ListParameterHistoryResponse)
  ))
_sym_db.RegisterMessage(ListParameterHistoryResponse)

GetParameterSamplesRequest = _reflection.GeneratedProtocolMessageType('GetParameterSamplesRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETPARAMETERSAMPLESREQUEST,
  __module__ = 'yamcs.protobuf.archive.archive_pb2'
  # @@protoc_insertion_point(class_scope:yamcs.protobuf.archive.GetParameterSamplesRequest)
  ))
_sym_db.RegisterMessage(GetParameterSamplesRequest)

ExportParameterValuesRequest = _reflection.GeneratedProtocolMessageType('ExportParameterValuesRequest', (_message.Message,), dict(
  DESCRIPTOR = _EXPORTPARAMETERVALUESREQUEST,
  __module__ = 'yamcs.protobuf.archive.archive_pb2'
  # @@protoc_insertion_point(class_scope:yamcs.protobuf.archive.ExportParameterValuesRequest)
  ))
_sym_db.RegisterMessage(ExportParameterValuesRequest)


DESCRIPTOR._options = None

_STREAMARCHIVEAPI = _descriptor.ServiceDescriptor(
  name='StreamArchiveApi',
  full_name='yamcs.protobuf.archive.StreamArchiveApi',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=1326,
  serialized_end=2224,
  methods=[
  _descriptor.MethodDescriptor(
    name='ListParameterGroups',
    full_name='yamcs.protobuf.archive.StreamArchiveApi.ListParameterGroups',
    index=0,
    containing_service=None,
    input_type=_LISTPARAMETERGROUPSREQUEST,
    output_type=_PARAMETERGROUPINFO,
    serialized_options=_b('\212\222\003*\n(/api/archive/{instance}/parameter-groups'),
  ),
  _descriptor.MethodDescriptor(
    name='ListParameterHistory',
    full_name='yamcs.protobuf.archive.StreamArchiveApi.ListParameterHistory',
    index=1,
    containing_service=None,
    input_type=_LISTPARAMETERHISTORYREQUEST,
    output_type=_LISTPARAMETERHISTORYRESPONSE,
    serialized_options=_b('\212\222\0033\n1/api/stream-archive/{instance}/parameters/{name*}'),
  ),
  _descriptor.MethodDescriptor(
    name='StreamParameterValues',
    full_name='yamcs.protobuf.archive.StreamArchiveApi.StreamParameterValues',
    index=2,
    containing_service=None,
    input_type=_STREAMPARAMETERVALUESREQUEST,
    output_type=yamcs_dot_protobuf_dot_pvalue_dot_pvalue__pb2._PARAMETERDATA,
    serialized_options=_b('\212\222\0039\0324/api/stream-archive/{instance}:streamParameterValues:\001*'),
  ),
  _descriptor.MethodDescriptor(
    name='GetParameterSamples',
    full_name='yamcs.protobuf.archive.StreamArchiveApi.GetParameterSamples',
    index=3,
    containing_service=None,
    input_type=_GETPARAMETERSAMPLESREQUEST,
    output_type=yamcs_dot_protobuf_dot_pvalue_dot_pvalue__pb2._TIMESERIES,
    serialized_options=_b('\212\222\003C\n9/api/stream-archive/{instance}/parameters/{name*}/samplesR\006sample'),
  ),
  _descriptor.MethodDescriptor(
    name='ExportParameterValues',
    full_name='yamcs.protobuf.archive.StreamArchiveApi.ExportParameterValues',
    index=4,
    containing_service=None,
    input_type=_EXPORTPARAMETERVALUESREQUEST,
    output_type=yamcs_dot_api_dot_httpbody__pb2._HTTPBODY,
    serialized_options=_b('\212\222\003/\n-/api/archive/{instance}:exportParameterValues'),
  ),
])
_sym_db.RegisterServiceDescriptor(_STREAMARCHIVEAPI)

DESCRIPTOR.services_by_name['StreamArchiveApi'] = _STREAMARCHIVEAPI

# @@protoc_insertion_point(module_scope)
