# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yamcs/protobuf/events/events_service.proto

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
from yamcs.protobuf.events import events_pb2 as yamcs_dot_protobuf_dot_events_dot_events__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='yamcs/protobuf/events/events_service.proto',
  package='yamcs.protobuf.events',
  syntax='proto2',
  serialized_options=_b('\n\022org.yamcs.protobufB\022EventsServiceProtoP\001'),
  serialized_pb=_b('\n*yamcs/protobuf/events/events_service.proto\x12\x15yamcs.protobuf.events\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1byamcs/api/annotations.proto\x1a\x18yamcs/api/httpbody.proto\x1a\"yamcs/protobuf/events/events.proto\"\xe0\x01\n\x11ListEventsRequest\x12\x10\n\x08instance\x18\x01 \x01(\t\x12\x0b\n\x03pos\x18\x02 \x01(\x03\x12\r\n\x05limit\x18\x03 \x01(\x05\x12\r\n\x05order\x18\x04 \x01(\t\x12\x10\n\x08severity\x18\x05 \x01(\t\x12\x0e\n\x06source\x18\x06 \x03(\t\x12\x0c\n\x04next\x18\x07 \x01(\t\x12)\n\x05start\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12(\n\x04stop\x18\t \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\t\n\x01q\x18\n \x01(\t\"\\\n\x12ListEventsResponse\x12+\n\x05\x65vent\x18\x01 \x03(\x0b\x32\x1c.yamcs.protobuf.events.Event\x12\x19\n\x11\x63ontinuationToken\x18\x02 \x01(\t\"*\n\x16SubscribeEventsRequest\x12\x10\n\x08instance\x18\x01 \x01(\t\"\xa9\x01\n\x12\x43reateEventRequest\x12\x10\n\x08instance\x18\x01 \x01(\t\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\x12\x10\n\x08severity\x18\x04 \x01(\t\x12(\n\x04time\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0e\n\x06source\x18\x06 \x01(\t\x12\x16\n\x0esequenceNumber\x18\x07 \x01(\x05\"\xa9\x01\n\x13StreamEventsRequest\x12\x10\n\x08instance\x18\x01 \x01(\t\x12)\n\x05start\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12(\n\x04stop\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0e\n\x06source\x18\x04 \x03(\t\x12\x10\n\x08severity\x18\x05 \x01(\t\x12\t\n\x01q\x18\x06 \x01(\t\"+\n\x17ListEventSourcesRequest\x12\x10\n\x08instance\x18\x01 \x01(\t\"*\n\x18ListEventSourcesResponse\x12\x0e\n\x06source\x18\x01 \x03(\t\"\xbc\x01\n\x13\x45xportEventsRequest\x12\x10\n\x08instance\x18\x01 \x01(\t\x12)\n\x05start\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12(\n\x04stop\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0e\n\x06source\x18\x04 \x03(\t\x12\x10\n\x08severity\x18\x05 \x01(\t\x12\t\n\x01q\x18\x06 \x01(\t\x12\x11\n\tdelimiter\x18\x07 \x01(\t2\xbc\x06\n\tEventsApi\x12\x87\x01\n\nListEvents\x12(.yamcs.protobuf.events.ListEventsRequest\x1a).yamcs.protobuf.events.ListEventsResponse\"$\x8a\x92\x03 \n\x1e/api/archive/{instance}/events\x12\x7f\n\x0b\x43reateEvent\x12).yamcs.protobuf.events.CreateEventRequest\x1a\x1c.yamcs.protobuf.events.Event\"\'\x8a\x92\x03#\x1a\x1e/api/archive/{instance}/events:\x01*\x12\xa1\x01\n\x10ListEventSources\x12..yamcs.protobuf.events.ListEventSourcesRequest\x1a/.yamcs.protobuf.events.ListEventSourcesResponse\",\x8a\x92\x03(\n&/api/archive/{instance}/events/sources\x12\x90\x01\n\x0cStreamEvents\x12*.yamcs.protobuf.events.StreamEventsRequest\x1a\x1c.yamcs.protobuf.events.Event\"4\x8a\x92\x03\x30\x1a+/api/stream-archive/{instance}:streamEvents:\x01*0\x01\x12}\n\x0c\x45xportEvents\x12*.yamcs.protobuf.events.ExportEventsRequest\x1a\x13.yamcs.api.HttpBody\"*\x8a\x92\x03&\n$/api/archive/{instance}:exportEvents0\x01\x12n\n\x0fSubscribeEvents\x12-.yamcs.protobuf.events.SubscribeEventsRequest\x1a\x1c.yamcs.protobuf.events.Event\"\x0c\xda\x92\x03\x08\n\x06\x65vents0\x01\x42*\n\x12org.yamcs.protobufB\x12\x45ventsServiceProtoP\x01')
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,yamcs_dot_api_dot_annotations__pb2.DESCRIPTOR,yamcs_dot_api_dot_httpbody__pb2.DESCRIPTOR,yamcs_dot_protobuf_dot_events_dot_events__pb2.DESCRIPTOR,])




_LISTEVENTSREQUEST = _descriptor.Descriptor(
  name='ListEventsRequest',
  full_name='yamcs.protobuf.events.ListEventsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='instance', full_name='yamcs.protobuf.events.ListEventsRequest.instance', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pos', full_name='yamcs.protobuf.events.ListEventsRequest.pos', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='limit', full_name='yamcs.protobuf.events.ListEventsRequest.limit', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='order', full_name='yamcs.protobuf.events.ListEventsRequest.order', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='severity', full_name='yamcs.protobuf.events.ListEventsRequest.severity', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='source', full_name='yamcs.protobuf.events.ListEventsRequest.source', index=5,
      number=6, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='next', full_name='yamcs.protobuf.events.ListEventsRequest.next', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='start', full_name='yamcs.protobuf.events.ListEventsRequest.start', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stop', full_name='yamcs.protobuf.events.ListEventsRequest.stop', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='q', full_name='yamcs.protobuf.events.ListEventsRequest.q', index=9,
      number=10, type=9, cpp_type=9, label=1,
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
  serialized_start=194,
  serialized_end=418,
)


_LISTEVENTSRESPONSE = _descriptor.Descriptor(
  name='ListEventsResponse',
  full_name='yamcs.protobuf.events.ListEventsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='event', full_name='yamcs.protobuf.events.ListEventsResponse.event', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='continuationToken', full_name='yamcs.protobuf.events.ListEventsResponse.continuationToken', index=1,
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
  serialized_start=420,
  serialized_end=512,
)


_SUBSCRIBEEVENTSREQUEST = _descriptor.Descriptor(
  name='SubscribeEventsRequest',
  full_name='yamcs.protobuf.events.SubscribeEventsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='instance', full_name='yamcs.protobuf.events.SubscribeEventsRequest.instance', index=0,
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
  serialized_start=514,
  serialized_end=556,
)


_CREATEEVENTREQUEST = _descriptor.Descriptor(
  name='CreateEventRequest',
  full_name='yamcs.protobuf.events.CreateEventRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='instance', full_name='yamcs.protobuf.events.CreateEventRequest.instance', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='yamcs.protobuf.events.CreateEventRequest.type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='message', full_name='yamcs.protobuf.events.CreateEventRequest.message', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='severity', full_name='yamcs.protobuf.events.CreateEventRequest.severity', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='time', full_name='yamcs.protobuf.events.CreateEventRequest.time', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='source', full_name='yamcs.protobuf.events.CreateEventRequest.source', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sequenceNumber', full_name='yamcs.protobuf.events.CreateEventRequest.sequenceNumber', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=559,
  serialized_end=728,
)


_STREAMEVENTSREQUEST = _descriptor.Descriptor(
  name='StreamEventsRequest',
  full_name='yamcs.protobuf.events.StreamEventsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='instance', full_name='yamcs.protobuf.events.StreamEventsRequest.instance', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='start', full_name='yamcs.protobuf.events.StreamEventsRequest.start', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stop', full_name='yamcs.protobuf.events.StreamEventsRequest.stop', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='source', full_name='yamcs.protobuf.events.StreamEventsRequest.source', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='severity', full_name='yamcs.protobuf.events.StreamEventsRequest.severity', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='q', full_name='yamcs.protobuf.events.StreamEventsRequest.q', index=5,
      number=6, type=9, cpp_type=9, label=1,
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
  serialized_start=731,
  serialized_end=900,
)


_LISTEVENTSOURCESREQUEST = _descriptor.Descriptor(
  name='ListEventSourcesRequest',
  full_name='yamcs.protobuf.events.ListEventSourcesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='instance', full_name='yamcs.protobuf.events.ListEventSourcesRequest.instance', index=0,
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
  serialized_start=902,
  serialized_end=945,
)


_LISTEVENTSOURCESRESPONSE = _descriptor.Descriptor(
  name='ListEventSourcesResponse',
  full_name='yamcs.protobuf.events.ListEventSourcesResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='source', full_name='yamcs.protobuf.events.ListEventSourcesResponse.source', index=0,
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
  serialized_start=947,
  serialized_end=989,
)


_EXPORTEVENTSREQUEST = _descriptor.Descriptor(
  name='ExportEventsRequest',
  full_name='yamcs.protobuf.events.ExportEventsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='instance', full_name='yamcs.protobuf.events.ExportEventsRequest.instance', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='start', full_name='yamcs.protobuf.events.ExportEventsRequest.start', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stop', full_name='yamcs.protobuf.events.ExportEventsRequest.stop', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='source', full_name='yamcs.protobuf.events.ExportEventsRequest.source', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='severity', full_name='yamcs.protobuf.events.ExportEventsRequest.severity', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='q', full_name='yamcs.protobuf.events.ExportEventsRequest.q', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='delimiter', full_name='yamcs.protobuf.events.ExportEventsRequest.delimiter', index=6,
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
  serialized_start=992,
  serialized_end=1180,
)

_LISTEVENTSREQUEST.fields_by_name['start'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_LISTEVENTSREQUEST.fields_by_name['stop'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_LISTEVENTSRESPONSE.fields_by_name['event'].message_type = yamcs_dot_protobuf_dot_events_dot_events__pb2._EVENT
_CREATEEVENTREQUEST.fields_by_name['time'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_STREAMEVENTSREQUEST.fields_by_name['start'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_STREAMEVENTSREQUEST.fields_by_name['stop'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_EXPORTEVENTSREQUEST.fields_by_name['start'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_EXPORTEVENTSREQUEST.fields_by_name['stop'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
DESCRIPTOR.message_types_by_name['ListEventsRequest'] = _LISTEVENTSREQUEST
DESCRIPTOR.message_types_by_name['ListEventsResponse'] = _LISTEVENTSRESPONSE
DESCRIPTOR.message_types_by_name['SubscribeEventsRequest'] = _SUBSCRIBEEVENTSREQUEST
DESCRIPTOR.message_types_by_name['CreateEventRequest'] = _CREATEEVENTREQUEST
DESCRIPTOR.message_types_by_name['StreamEventsRequest'] = _STREAMEVENTSREQUEST
DESCRIPTOR.message_types_by_name['ListEventSourcesRequest'] = _LISTEVENTSOURCESREQUEST
DESCRIPTOR.message_types_by_name['ListEventSourcesResponse'] = _LISTEVENTSOURCESRESPONSE
DESCRIPTOR.message_types_by_name['ExportEventsRequest'] = _EXPORTEVENTSREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ListEventsRequest = _reflection.GeneratedProtocolMessageType('ListEventsRequest', (_message.Message,), dict(
  DESCRIPTOR = _LISTEVENTSREQUEST,
  __module__ = 'yamcs.protobuf.events.events_service_pb2'
  # @@protoc_insertion_point(class_scope:yamcs.protobuf.events.ListEventsRequest)
  ))
_sym_db.RegisterMessage(ListEventsRequest)

ListEventsResponse = _reflection.GeneratedProtocolMessageType('ListEventsResponse', (_message.Message,), dict(
  DESCRIPTOR = _LISTEVENTSRESPONSE,
  __module__ = 'yamcs.protobuf.events.events_service_pb2'
  # @@protoc_insertion_point(class_scope:yamcs.protobuf.events.ListEventsResponse)
  ))
_sym_db.RegisterMessage(ListEventsResponse)

SubscribeEventsRequest = _reflection.GeneratedProtocolMessageType('SubscribeEventsRequest', (_message.Message,), dict(
  DESCRIPTOR = _SUBSCRIBEEVENTSREQUEST,
  __module__ = 'yamcs.protobuf.events.events_service_pb2'
  # @@protoc_insertion_point(class_scope:yamcs.protobuf.events.SubscribeEventsRequest)
  ))
_sym_db.RegisterMessage(SubscribeEventsRequest)

CreateEventRequest = _reflection.GeneratedProtocolMessageType('CreateEventRequest', (_message.Message,), dict(
  DESCRIPTOR = _CREATEEVENTREQUEST,
  __module__ = 'yamcs.protobuf.events.events_service_pb2'
  # @@protoc_insertion_point(class_scope:yamcs.protobuf.events.CreateEventRequest)
  ))
_sym_db.RegisterMessage(CreateEventRequest)

StreamEventsRequest = _reflection.GeneratedProtocolMessageType('StreamEventsRequest', (_message.Message,), dict(
  DESCRIPTOR = _STREAMEVENTSREQUEST,
  __module__ = 'yamcs.protobuf.events.events_service_pb2'
  # @@protoc_insertion_point(class_scope:yamcs.protobuf.events.StreamEventsRequest)
  ))
_sym_db.RegisterMessage(StreamEventsRequest)

ListEventSourcesRequest = _reflection.GeneratedProtocolMessageType('ListEventSourcesRequest', (_message.Message,), dict(
  DESCRIPTOR = _LISTEVENTSOURCESREQUEST,
  __module__ = 'yamcs.protobuf.events.events_service_pb2'
  # @@protoc_insertion_point(class_scope:yamcs.protobuf.events.ListEventSourcesRequest)
  ))
_sym_db.RegisterMessage(ListEventSourcesRequest)

ListEventSourcesResponse = _reflection.GeneratedProtocolMessageType('ListEventSourcesResponse', (_message.Message,), dict(
  DESCRIPTOR = _LISTEVENTSOURCESRESPONSE,
  __module__ = 'yamcs.protobuf.events.events_service_pb2'
  # @@protoc_insertion_point(class_scope:yamcs.protobuf.events.ListEventSourcesResponse)
  ))
_sym_db.RegisterMessage(ListEventSourcesResponse)

ExportEventsRequest = _reflection.GeneratedProtocolMessageType('ExportEventsRequest', (_message.Message,), dict(
  DESCRIPTOR = _EXPORTEVENTSREQUEST,
  __module__ = 'yamcs.protobuf.events.events_service_pb2'
  # @@protoc_insertion_point(class_scope:yamcs.protobuf.events.ExportEventsRequest)
  ))
_sym_db.RegisterMessage(ExportEventsRequest)


DESCRIPTOR._options = None

_EVENTSAPI = _descriptor.ServiceDescriptor(
  name='EventsApi',
  full_name='yamcs.protobuf.events.EventsApi',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=1183,
  serialized_end=2011,
  methods=[
  _descriptor.MethodDescriptor(
    name='ListEvents',
    full_name='yamcs.protobuf.events.EventsApi.ListEvents',
    index=0,
    containing_service=None,
    input_type=_LISTEVENTSREQUEST,
    output_type=_LISTEVENTSRESPONSE,
    serialized_options=_b('\212\222\003 \n\036/api/archive/{instance}/events'),
  ),
  _descriptor.MethodDescriptor(
    name='CreateEvent',
    full_name='yamcs.protobuf.events.EventsApi.CreateEvent',
    index=1,
    containing_service=None,
    input_type=_CREATEEVENTREQUEST,
    output_type=yamcs_dot_protobuf_dot_events_dot_events__pb2._EVENT,
    serialized_options=_b('\212\222\003#\032\036/api/archive/{instance}/events:\001*'),
  ),
  _descriptor.MethodDescriptor(
    name='ListEventSources',
    full_name='yamcs.protobuf.events.EventsApi.ListEventSources',
    index=2,
    containing_service=None,
    input_type=_LISTEVENTSOURCESREQUEST,
    output_type=_LISTEVENTSOURCESRESPONSE,
    serialized_options=_b('\212\222\003(\n&/api/archive/{instance}/events/sources'),
  ),
  _descriptor.MethodDescriptor(
    name='StreamEvents',
    full_name='yamcs.protobuf.events.EventsApi.StreamEvents',
    index=3,
    containing_service=None,
    input_type=_STREAMEVENTSREQUEST,
    output_type=yamcs_dot_protobuf_dot_events_dot_events__pb2._EVENT,
    serialized_options=_b('\212\222\0030\032+/api/stream-archive/{instance}:streamEvents:\001*'),
  ),
  _descriptor.MethodDescriptor(
    name='ExportEvents',
    full_name='yamcs.protobuf.events.EventsApi.ExportEvents',
    index=4,
    containing_service=None,
    input_type=_EXPORTEVENTSREQUEST,
    output_type=yamcs_dot_api_dot_httpbody__pb2._HTTPBODY,
    serialized_options=_b('\212\222\003&\n$/api/archive/{instance}:exportEvents'),
  ),
  _descriptor.MethodDescriptor(
    name='SubscribeEvents',
    full_name='yamcs.protobuf.events.EventsApi.SubscribeEvents',
    index=5,
    containing_service=None,
    input_type=_SUBSCRIBEEVENTSREQUEST,
    output_type=yamcs_dot_protobuf_dot_events_dot_events__pb2._EVENT,
    serialized_options=_b('\332\222\003\010\n\006events'),
  ),
])
_sym_db.RegisterServiceDescriptor(_EVENTSAPI)

DESCRIPTOR.services_by_name['EventsApi'] = _EVENTSAPI

# @@protoc_insertion_point(module_scope)
