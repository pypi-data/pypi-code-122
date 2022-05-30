# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: counter.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rcounter.proto\x12\x07\x63ounter\"\x85\x01\n\x14\x43reateAccountRequest\x12\r\n\x05owner\x18\x01 \x01(\t\x12\x34\n\x04kind\x18\x02 \x01(\x0e\x32&.counter.CreateAccountRequest.KindType\x12\x0c\n\x04name\x18\x03 \x01(\t\"\x1a\n\x08KindType\x12\x06\n\x02PS\x10\x00\x12\x06\n\x02\x43O\x10\x01\"\xc8\x01\n\x0f\x41\x63\x63ountResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05\x61\x63\x63no\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x0f\n\x07\x62\x61lance\x18\x04 \x01(\x02\x12\x0e\n\x06\x63redit\x18\x05 \x01(\x02\x12\x0f\n\x07warning\x18\x06 \x01(\x02\x12\r\n\x05state\x18\x07 \x01(\t\x12/\n\x04kind\x18\x08 \x01(\x0e\x32!.counter.AccountResponse.KindType\"\x1a\n\x08KindType\x12\x06\n\x02PS\x10\x00\x12\x06\n\x02\x43O\x10\x01\"T\n\x13QueryAccountRequest\x12\x0e\n\x06userid\x18\x01 \x01(\t\x12\x15\n\rapplicationid\x18\x02 \x01(\t\x12\x16\n\x0eorganizationid\x18\x03 \x01(\t\"C\n\x14UsableServiceRequest\x12\r\n\x05\x61\x63\x63no\x18\x01 \x01(\t\x12\r\n\x05label\x18\x02 \x01(\t\x12\r\n\x05\x63ount\x18\x03 \x01(\x05\"\'\n\x15UsableServiceResponse\x12\x0e\n\x06usable\x18\x01 \x01(\x08\"\xc6\x01\n\x13StartServiceRequest\x12\r\n\x05\x61\x63\x63no\x18\x01 \x01(\t\x12\r\n\x05label\x18\x02 \x01(\t\x12\x12\n\nstart_time\x18\x03 \x01(\t\x12\r\n\x05\x63ount\x18\x04 \x01(\x05\x12\x12\n\nproviderno\x18\x05 \x01(\t\x12\x0f\n\x07summary\x18\x06 \x01(\t\x12\x13\n\x0b\x61pplication\x18\x07 \x01(\t\x12\x14\n\x0corganization\x18\x08 \x01(\t\x12\x0e\n\x06\x65xpire\x18\t \x01(\t\x12\x0e\n\x06usable\x18\n \x01(\x08\"5\n\x14StartServiceResponse\x12\r\n\x05svcno\x18\x01 \x01(\t\x12\x0e\n\x06\x65xpire\x18\x02 \x01(\t\"\xc8\x01\n\x11\x45ndServiceRequest\x12\r\n\x05\x61\x63\x63no\x18\x01 \x01(\t\x12\r\n\x05svcno\x18\x02 \x01(\t\x12\r\n\x05label\x18\x03 \x01(\t\x12\x12\n\nstart_time\x18\x04 \x01(\t\x12\x13\n\x0b\x66inish_time\x18\x05 \x01(\t\x12\r\n\x05\x63ount\x18\x06 \x01(\x05\x12\x12\n\nproviderno\x18\x07 \x01(\t\x12\x0f\n\x07summary\x18\x08 \x01(\t\x12\x13\n\x0b\x61pplication\x18\t \x01(\t\x12\x14\n\x0corganization\x18\n \x01(\t\"i\n\x12\x45ndServiceResponse\x12\r\n\x05svcno\x18\x01 \x01(\t\x12\x12\n\nstart_time\x18\x02 \x01(\t\x12\x13\n\x0b\x66inish_time\x18\x03 \x01(\t\x12\r\n\x05\x63ount\x18\x04 \x01(\x02\x12\x0c\n\x04\x63ost\x18\x05 \x01(\x02\"M\n\x0fResourceRequest\x12\r\n\x05\x61\x63\x63no\x18\x01 \x01(\t\x12\r\n\x05label\x18\x02 \x01(\t\x12\r\n\x05\x63ount\x18\x03 \x01(\x05\x12\r\n\x05total\x18\x04 \x01(\x05\"1\n\x10ResourceResponse\x12\r\n\x05usage\x18\x01 \x01(\x05\x12\x0e\n\x06limits\x18\x02 \x01(\x05\"V\n\x12KeepServiceRequest\x12\r\n\x05\x61\x63\x63no\x18\x01 \x01(\t\x12\r\n\x05label\x18\x02 \x01(\t\x12\x12\n\nproviderno\x18\x03 \x01(\t\x12\x0e\n\x06\x65xpire\x18\x04 \x01(\t\"4\n\x13KeepServiceResponse\x12\x0e\n\x06\x65xpire\x18\x01 \x01(\t\x12\r\n\x05svcno\x18\x02 \x01(\t\":\n\x1aQueryAccountServiceRequest\x12\r\n\x05\x61\x63\x63no\x18\x01 \x01(\t\x12\r\n\x05label\x18\x02 \x01(\t\";\n\x1bQueryAccountServiceResponse\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x05\x12\x0e\n\x06\x64\x65tail\x18\x02 \x01(\t2\xd4\x05\n\x0e\x43ounterService\x12J\n\rCreateAccount\x12\x1d.counter.CreateAccountRequest\x1a\x18.counter.AccountResponse\"\x00\x12H\n\x0cQueryAccount\x12\x1c.counter.QueryAccountRequest\x1a\x18.counter.AccountResponse\"\x00\x12P\n\rUsableService\x12\x1d.counter.UsableServiceRequest\x1a\x1e.counter.UsableServiceResponse\"\x00\x12M\n\x0cStartService\x12\x1c.counter.StartServiceRequest\x1a\x1d.counter.StartServiceResponse\"\x00\x12G\n\nEndService\x12\x1a.counter.EndServiceRequest\x1a\x1b.counter.EndServiceResponse\"\x00\x12I\n\x10IncreaseResource\x12\x18.counter.ResourceRequest\x1a\x19.counter.ResourceResponse\"\x00\x12G\n\x0eReduceResource\x12\x18.counter.ResourceRequest\x1a\x19.counter.ResourceResponse\"\x00\x12J\n\x0bKeepService\x12\x1b.counter.KeepServiceRequest\x1a\x1c.counter.KeepServiceResponse\"\x00\x12\x62\n\x13QueryAccountService\x12#.counter.QueryAccountServiceRequest\x1a$.counter.QueryAccountServiceResponse\"\x00\x62\x06proto3')



_CREATEACCOUNTREQUEST = DESCRIPTOR.message_types_by_name['CreateAccountRequest']
_ACCOUNTRESPONSE = DESCRIPTOR.message_types_by_name['AccountResponse']
_QUERYACCOUNTREQUEST = DESCRIPTOR.message_types_by_name['QueryAccountRequest']
_USABLESERVICEREQUEST = DESCRIPTOR.message_types_by_name['UsableServiceRequest']
_USABLESERVICERESPONSE = DESCRIPTOR.message_types_by_name['UsableServiceResponse']
_STARTSERVICEREQUEST = DESCRIPTOR.message_types_by_name['StartServiceRequest']
_STARTSERVICERESPONSE = DESCRIPTOR.message_types_by_name['StartServiceResponse']
_ENDSERVICEREQUEST = DESCRIPTOR.message_types_by_name['EndServiceRequest']
_ENDSERVICERESPONSE = DESCRIPTOR.message_types_by_name['EndServiceResponse']
_RESOURCEREQUEST = DESCRIPTOR.message_types_by_name['ResourceRequest']
_RESOURCERESPONSE = DESCRIPTOR.message_types_by_name['ResourceResponse']
_KEEPSERVICEREQUEST = DESCRIPTOR.message_types_by_name['KeepServiceRequest']
_KEEPSERVICERESPONSE = DESCRIPTOR.message_types_by_name['KeepServiceResponse']
_QUERYACCOUNTSERVICEREQUEST = DESCRIPTOR.message_types_by_name['QueryAccountServiceRequest']
_QUERYACCOUNTSERVICERESPONSE = DESCRIPTOR.message_types_by_name['QueryAccountServiceResponse']
_CREATEACCOUNTREQUEST_KINDTYPE = _CREATEACCOUNTREQUEST.enum_types_by_name['KindType']
_ACCOUNTRESPONSE_KINDTYPE = _ACCOUNTRESPONSE.enum_types_by_name['KindType']
CreateAccountRequest = _reflection.GeneratedProtocolMessageType('CreateAccountRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEACCOUNTREQUEST,
  '__module__' : 'counter_pb2'
  # @@protoc_insertion_point(class_scope:counter.CreateAccountRequest)
  })
_sym_db.RegisterMessage(CreateAccountRequest)

AccountResponse = _reflection.GeneratedProtocolMessageType('AccountResponse', (_message.Message,), {
  'DESCRIPTOR' : _ACCOUNTRESPONSE,
  '__module__' : 'counter_pb2'
  # @@protoc_insertion_point(class_scope:counter.AccountResponse)
  })
_sym_db.RegisterMessage(AccountResponse)

QueryAccountRequest = _reflection.GeneratedProtocolMessageType('QueryAccountRequest', (_message.Message,), {
  'DESCRIPTOR' : _QUERYACCOUNTREQUEST,
  '__module__' : 'counter_pb2'
  # @@protoc_insertion_point(class_scope:counter.QueryAccountRequest)
  })
_sym_db.RegisterMessage(QueryAccountRequest)

UsableServiceRequest = _reflection.GeneratedProtocolMessageType('UsableServiceRequest', (_message.Message,), {
  'DESCRIPTOR' : _USABLESERVICEREQUEST,
  '__module__' : 'counter_pb2'
  # @@protoc_insertion_point(class_scope:counter.UsableServiceRequest)
  })
_sym_db.RegisterMessage(UsableServiceRequest)

UsableServiceResponse = _reflection.GeneratedProtocolMessageType('UsableServiceResponse', (_message.Message,), {
  'DESCRIPTOR' : _USABLESERVICERESPONSE,
  '__module__' : 'counter_pb2'
  # @@protoc_insertion_point(class_scope:counter.UsableServiceResponse)
  })
_sym_db.RegisterMessage(UsableServiceResponse)

StartServiceRequest = _reflection.GeneratedProtocolMessageType('StartServiceRequest', (_message.Message,), {
  'DESCRIPTOR' : _STARTSERVICEREQUEST,
  '__module__' : 'counter_pb2'
  # @@protoc_insertion_point(class_scope:counter.StartServiceRequest)
  })
_sym_db.RegisterMessage(StartServiceRequest)

StartServiceResponse = _reflection.GeneratedProtocolMessageType('StartServiceResponse', (_message.Message,), {
  'DESCRIPTOR' : _STARTSERVICERESPONSE,
  '__module__' : 'counter_pb2'
  # @@protoc_insertion_point(class_scope:counter.StartServiceResponse)
  })
_sym_db.RegisterMessage(StartServiceResponse)

EndServiceRequest = _reflection.GeneratedProtocolMessageType('EndServiceRequest', (_message.Message,), {
  'DESCRIPTOR' : _ENDSERVICEREQUEST,
  '__module__' : 'counter_pb2'
  # @@protoc_insertion_point(class_scope:counter.EndServiceRequest)
  })
_sym_db.RegisterMessage(EndServiceRequest)

EndServiceResponse = _reflection.GeneratedProtocolMessageType('EndServiceResponse', (_message.Message,), {
  'DESCRIPTOR' : _ENDSERVICERESPONSE,
  '__module__' : 'counter_pb2'
  # @@protoc_insertion_point(class_scope:counter.EndServiceResponse)
  })
_sym_db.RegisterMessage(EndServiceResponse)

ResourceRequest = _reflection.GeneratedProtocolMessageType('ResourceRequest', (_message.Message,), {
  'DESCRIPTOR' : _RESOURCEREQUEST,
  '__module__' : 'counter_pb2'
  # @@protoc_insertion_point(class_scope:counter.ResourceRequest)
  })
_sym_db.RegisterMessage(ResourceRequest)

ResourceResponse = _reflection.GeneratedProtocolMessageType('ResourceResponse', (_message.Message,), {
  'DESCRIPTOR' : _RESOURCERESPONSE,
  '__module__' : 'counter_pb2'
  # @@protoc_insertion_point(class_scope:counter.ResourceResponse)
  })
_sym_db.RegisterMessage(ResourceResponse)

KeepServiceRequest = _reflection.GeneratedProtocolMessageType('KeepServiceRequest', (_message.Message,), {
  'DESCRIPTOR' : _KEEPSERVICEREQUEST,
  '__module__' : 'counter_pb2'
  # @@protoc_insertion_point(class_scope:counter.KeepServiceRequest)
  })
_sym_db.RegisterMessage(KeepServiceRequest)

KeepServiceResponse = _reflection.GeneratedProtocolMessageType('KeepServiceResponse', (_message.Message,), {
  'DESCRIPTOR' : _KEEPSERVICERESPONSE,
  '__module__' : 'counter_pb2'
  # @@protoc_insertion_point(class_scope:counter.KeepServiceResponse)
  })
_sym_db.RegisterMessage(KeepServiceResponse)

QueryAccountServiceRequest = _reflection.GeneratedProtocolMessageType('QueryAccountServiceRequest', (_message.Message,), {
  'DESCRIPTOR' : _QUERYACCOUNTSERVICEREQUEST,
  '__module__' : 'counter_pb2'
  # @@protoc_insertion_point(class_scope:counter.QueryAccountServiceRequest)
  })
_sym_db.RegisterMessage(QueryAccountServiceRequest)

QueryAccountServiceResponse = _reflection.GeneratedProtocolMessageType('QueryAccountServiceResponse', (_message.Message,), {
  'DESCRIPTOR' : _QUERYACCOUNTSERVICERESPONSE,
  '__module__' : 'counter_pb2'
  # @@protoc_insertion_point(class_scope:counter.QueryAccountServiceResponse)
  })
_sym_db.RegisterMessage(QueryAccountServiceResponse)

_COUNTERSERVICE = DESCRIPTOR.services_by_name['CounterService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CREATEACCOUNTREQUEST._serialized_start=27
  _CREATEACCOUNTREQUEST._serialized_end=160
  _CREATEACCOUNTREQUEST_KINDTYPE._serialized_start=134
  _CREATEACCOUNTREQUEST_KINDTYPE._serialized_end=160
  _ACCOUNTRESPONSE._serialized_start=163
  _ACCOUNTRESPONSE._serialized_end=363
  _ACCOUNTRESPONSE_KINDTYPE._serialized_start=134
  _ACCOUNTRESPONSE_KINDTYPE._serialized_end=160
  _QUERYACCOUNTREQUEST._serialized_start=365
  _QUERYACCOUNTREQUEST._serialized_end=449
  _USABLESERVICEREQUEST._serialized_start=451
  _USABLESERVICEREQUEST._serialized_end=518
  _USABLESERVICERESPONSE._serialized_start=520
  _USABLESERVICERESPONSE._serialized_end=559
  _STARTSERVICEREQUEST._serialized_start=562
  _STARTSERVICEREQUEST._serialized_end=760
  _STARTSERVICERESPONSE._serialized_start=762
  _STARTSERVICERESPONSE._serialized_end=815
  _ENDSERVICEREQUEST._serialized_start=818
  _ENDSERVICEREQUEST._serialized_end=1018
  _ENDSERVICERESPONSE._serialized_start=1020
  _ENDSERVICERESPONSE._serialized_end=1125
  _RESOURCEREQUEST._serialized_start=1127
  _RESOURCEREQUEST._serialized_end=1204
  _RESOURCERESPONSE._serialized_start=1206
  _RESOURCERESPONSE._serialized_end=1255
  _KEEPSERVICEREQUEST._serialized_start=1257
  _KEEPSERVICEREQUEST._serialized_end=1343
  _KEEPSERVICERESPONSE._serialized_start=1345
  _KEEPSERVICERESPONSE._serialized_end=1397
  _QUERYACCOUNTSERVICEREQUEST._serialized_start=1399
  _QUERYACCOUNTSERVICEREQUEST._serialized_end=1457
  _QUERYACCOUNTSERVICERESPONSE._serialized_start=1459
  _QUERYACCOUNTSERVICERESPONSE._serialized_end=1518
  _COUNTERSERVICE._serialized_start=1521
  _COUNTERSERVICE._serialized_end=2245
# @@protoc_insertion_point(module_scope)
