# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yamcs/protobuf/events/events.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='yamcs/protobuf/events/events.proto',
  package='yamcs.protobuf.events',
  syntax='proto2',
  serialized_options=_b('\n\022org.yamcs.protobufB\013EventsProtoP\001'),
  serialized_pb=_b('\n\"yamcs/protobuf/events/events.proto\x12\x15yamcs.protobuf.events\x1a\x1fgoogle/protobuf/timestamp.proto\"\xf4\x02\n\x05\x45vent\x12\x0e\n\x06source\x18\x01 \x02(\t\x12\x32\n\x0egenerationTime\x18\x02 \x02(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x31\n\rreceptionTime\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x11\n\tseqNumber\x18\x04 \x01(\x05\x12\x0c\n\x04type\x18\x05 \x01(\t\x12\x0f\n\x07message\x18\x06 \x02(\t\x12\x42\n\x08severity\x18\x07 \x01(\x0e\x32*.yamcs.protobuf.events.Event.EventSeverity:\x04INFO\x12\x11\n\tcreatedBy\x18\n \x01(\t\"d\n\rEventSeverity\x12\x08\n\x04INFO\x10\x00\x12\x0b\n\x07WARNING\x10\x01\x12\t\n\x05\x45RROR\x10\x02\x12\t\n\x05WATCH\x10\x03\x12\x0c\n\x08\x44ISTRESS\x10\x05\x12\x0c\n\x08\x43RITICAL\x10\x06\x12\n\n\x06SEVERE\x10\x07*\x05\x08\x64\x10\x91NB#\n\x12org.yamcs.protobufB\x0b\x45ventsProtoP\x01')
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])



_EVENT_EVENTSEVERITY = _descriptor.EnumDescriptor(
  name='EventSeverity',
  full_name='yamcs.protobuf.events.Event.EventSeverity',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='INFO', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WARNING', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WATCH', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DISTRESS', index=4, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CRITICAL', index=5, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SEVERE', index=6, number=7,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=360,
  serialized_end=460,
)
_sym_db.RegisterEnumDescriptor(_EVENT_EVENTSEVERITY)


_EVENT = _descriptor.Descriptor(
  name='Event',
  full_name='yamcs.protobuf.events.Event',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='source', full_name='yamcs.protobuf.events.Event.source', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='generationTime', full_name='yamcs.protobuf.events.Event.generationTime', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='receptionTime', full_name='yamcs.protobuf.events.Event.receptionTime', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='seqNumber', full_name='yamcs.protobuf.events.Event.seqNumber', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='yamcs.protobuf.events.Event.type', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='message', full_name='yamcs.protobuf.events.Event.message', index=5,
      number=6, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='severity', full_name='yamcs.protobuf.events.Event.severity', index=6,
      number=7, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='createdBy', full_name='yamcs.protobuf.events.Event.createdBy', index=7,
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
    _EVENT_EVENTSEVERITY,
  ],
  serialized_options=None,
  is_extendable=True,
  syntax='proto2',
  extension_ranges=[(100, 10001), ],
  oneofs=[
  ],
  serialized_start=95,
  serialized_end=467,
)

_EVENT.fields_by_name['generationTime'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_EVENT.fields_by_name['receptionTime'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_EVENT.fields_by_name['severity'].enum_type = _EVENT_EVENTSEVERITY
_EVENT_EVENTSEVERITY.containing_type = _EVENT
DESCRIPTOR.message_types_by_name['Event'] = _EVENT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Event = _reflection.GeneratedProtocolMessageType('Event', (_message.Message,), dict(
  DESCRIPTOR = _EVENT,
  __module__ = 'yamcs.protobuf.events.events_pb2'
  # @@protoc_insertion_point(class_scope:yamcs.protobuf.events.Event)
  ))
_sym_db.RegisterMessage(Event)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
