# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nanopb.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cnanopb.proto\x1a google/protobuf/descriptor.proto\"\xa4\x07\n\rNanoPBOptions\x12\x10\n\x08max_size\x18\x01 \x01(\x05\x12\x12\n\nmax_length\x18\x0e \x01(\x05\x12\x11\n\tmax_count\x18\x02 \x01(\x05\x12&\n\x08int_size\x18\x07 \x01(\x0e\x32\x08.IntSize:\nIS_DEFAULT\x12$\n\x04type\x18\x03 \x01(\x0e\x32\n.FieldType:\nFT_DEFAULT\x12\x18\n\nlong_names\x18\x04 \x01(\x08:\x04true\x12\x1c\n\rpacked_struct\x18\x05 \x01(\x08:\x05\x66\x61lse\x12\x1a\n\x0bpacked_enum\x18\n \x01(\x08:\x05\x66\x61lse\x12\x1b\n\x0cskip_message\x18\x06 \x01(\x08:\x05\x66\x61lse\x12\x18\n\tno_unions\x18\x08 \x01(\x08:\x05\x66\x61lse\x12\r\n\x05msgid\x18\t \x01(\r\x12\x1e\n\x0f\x61nonymous_oneof\x18\x0b \x01(\x08:\x05\x66\x61lse\x12\x15\n\x06proto3\x18\x0c \x01(\x08:\x05\x66\x61lse\x12#\n\x14proto3_singular_msgs\x18\x15 \x01(\x08:\x05\x66\x61lse\x12\x1d\n\x0e\x65num_to_string\x18\r \x01(\x08:\x05\x66\x61lse\x12\x1b\n\x0c\x66ixed_length\x18\x0f \x01(\x08:\x05\x66\x61lse\x12\x1a\n\x0b\x66ixed_count\x18\x10 \x01(\x08:\x05\x66\x61lse\x12\x1e\n\x0fsubmsg_callback\x18\x16 \x01(\x08:\x05\x66\x61lse\x12/\n\x0cmangle_names\x18\x11 \x01(\x0e\x32\x11.TypenameMangling:\x06M_NONE\x12(\n\x11\x63\x61llback_datatype\x18\x12 \x01(\t:\rpb_callback_t\x12\x34\n\x11\x63\x61llback_function\x18\x13 \x01(\t:\x19pb_default_field_callback\x12\x30\n\x0e\x64\x65scriptorsize\x18\x14 \x01(\x0e\x32\x0f.DescriptorSize:\x07\x44S_AUTO\x12\x1a\n\x0b\x64\x65\x66\x61ult_has\x18\x17 \x01(\x08:\x05\x66\x61lse\x12\x0f\n\x07include\x18\x18 \x03(\t\x12\x0f\n\x07\x65xclude\x18\x1a \x03(\t\x12\x0f\n\x07package\x18\x19 \x01(\t\x12\x41\n\rtype_override\x18\x1b \x01(\x0e\x32*.google.protobuf.FieldDescriptorProto.Type\x12\x19\n\x0bsort_by_tag\x18\x1c \x01(\x08:\x04true\x12.\n\rfallback_type\x18\x1d \x01(\x0e\x32\n.FieldType:\x0b\x46T_CALLBACK*i\n\tFieldType\x12\x0e\n\nFT_DEFAULT\x10\x00\x12\x0f\n\x0b\x46T_CALLBACK\x10\x01\x12\x0e\n\nFT_POINTER\x10\x04\x12\r\n\tFT_STATIC\x10\x02\x12\r\n\tFT_IGNORE\x10\x03\x12\r\n\tFT_INLINE\x10\x05*D\n\x07IntSize\x12\x0e\n\nIS_DEFAULT\x10\x00\x12\x08\n\x04IS_8\x10\x08\x12\t\n\x05IS_16\x10\x10\x12\t\n\x05IS_32\x10 \x12\t\n\x05IS_64\x10@*Z\n\x10TypenameMangling\x12\n\n\x06M_NONE\x10\x00\x12\x13\n\x0fM_STRIP_PACKAGE\x10\x01\x12\r\n\tM_FLATTEN\x10\x02\x12\x16\n\x12M_PACKAGE_INITIALS\x10\x03*E\n\x0e\x44\x65scriptorSize\x12\x0b\n\x07\x44S_AUTO\x10\x00\x12\x08\n\x04\x44S_1\x10\x01\x12\x08\n\x04\x44S_2\x10\x02\x12\x08\n\x04\x44S_4\x10\x04\x12\x08\n\x04\x44S_8\x10\x08:E\n\x0enanopb_fileopt\x12\x1c.google.protobuf.FileOptions\x18\xf2\x07 \x01(\x0b\x32\x0e.NanoPBOptions:G\n\rnanopb_msgopt\x12\x1f.google.protobuf.MessageOptions\x18\xf2\x07 \x01(\x0b\x32\x0e.NanoPBOptions:E\n\x0enanopb_enumopt\x12\x1c.google.protobuf.EnumOptions\x18\xf2\x07 \x01(\x0b\x32\x0e.NanoPBOptions:>\n\x06nanopb\x12\x1d.google.protobuf.FieldOptions\x18\xf2\x07 \x01(\x0b\x32\x0e.NanoPBOptionsB\x1a\n\x18\x66i.kapsi.koti.jpa.nanopb')

_FIELDTYPE = DESCRIPTOR.enum_types_by_name['FieldType']
FieldType = enum_type_wrapper.EnumTypeWrapper(_FIELDTYPE)
_INTSIZE = DESCRIPTOR.enum_types_by_name['IntSize']
IntSize = enum_type_wrapper.EnumTypeWrapper(_INTSIZE)
_TYPENAMEMANGLING = DESCRIPTOR.enum_types_by_name['TypenameMangling']
TypenameMangling = enum_type_wrapper.EnumTypeWrapper(_TYPENAMEMANGLING)
_DESCRIPTORSIZE = DESCRIPTOR.enum_types_by_name['DescriptorSize']
DescriptorSize = enum_type_wrapper.EnumTypeWrapper(_DESCRIPTORSIZE)
FT_DEFAULT = 0
FT_CALLBACK = 1
FT_POINTER = 4
FT_STATIC = 2
FT_IGNORE = 3
FT_INLINE = 5
IS_DEFAULT = 0
IS_8 = 8
IS_16 = 16
IS_32 = 32
IS_64 = 64
M_NONE = 0
M_STRIP_PACKAGE = 1
M_FLATTEN = 2
M_PACKAGE_INITIALS = 3
DS_AUTO = 0
DS_1 = 1
DS_2 = 2
DS_4 = 4
DS_8 = 8

NANOPB_FILEOPT_FIELD_NUMBER = 1010
nanopb_fileopt = DESCRIPTOR.extensions_by_name['nanopb_fileopt']
NANOPB_MSGOPT_FIELD_NUMBER = 1010
nanopb_msgopt = DESCRIPTOR.extensions_by_name['nanopb_msgopt']
NANOPB_ENUMOPT_FIELD_NUMBER = 1010
nanopb_enumopt = DESCRIPTOR.extensions_by_name['nanopb_enumopt']
NANOPB_FIELD_NUMBER = 1010
nanopb = DESCRIPTOR.extensions_by_name['nanopb']

_NANOPBOPTIONS = DESCRIPTOR.message_types_by_name['NanoPBOptions']
NanoPBOptions = _reflection.GeneratedProtocolMessageType('NanoPBOptions', (_message.Message,), {
  'DESCRIPTOR' : _NANOPBOPTIONS,
  '__module__' : 'nanopb_pb2'
  # @@protoc_insertion_point(class_scope:NanoPBOptions)
  })
_sym_db.RegisterMessage(NanoPBOptions)

if _descriptor._USE_C_DESCRIPTORS == False:
  google_dot_protobuf_dot_descriptor__pb2.FileOptions.RegisterExtension(nanopb_fileopt)
  google_dot_protobuf_dot_descriptor__pb2.MessageOptions.RegisterExtension(nanopb_msgopt)
  google_dot_protobuf_dot_descriptor__pb2.EnumOptions.RegisterExtension(nanopb_enumopt)
  google_dot_protobuf_dot_descriptor__pb2.FieldOptions.RegisterExtension(nanopb)

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\030fi.kapsi.koti.jpa.nanopb'
  _FIELDTYPE._serialized_start=985
  _FIELDTYPE._serialized_end=1090
  _INTSIZE._serialized_start=1092
  _INTSIZE._serialized_end=1160
  _TYPENAMEMANGLING._serialized_start=1162
  _TYPENAMEMANGLING._serialized_end=1252
  _DESCRIPTORSIZE._serialized_start=1254
  _DESCRIPTORSIZE._serialized_end=1323
  _NANOPBOPTIONS._serialized_start=51
  _NANOPBOPTIONS._serialized_end=983
# @@protoc_insertion_point(module_scope)
