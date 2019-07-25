# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: txn.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='txn.proto',
  package='CMD',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\ttxn.proto\x12\x03\x43MD\"\x1c\n\x08txnParam\x12\x10\n\x08priority\x18\x01 \x01(\x04\"|\n\x07txnData\x12\x10\n\x08\x63lientID\x18\x01 \x01(\x04\x12\x15\n\rtransactionID\x18\x02 \x01(\x04\x12\x11\n\tsessionID\x18\x03 \x01(\x04\x12\x0e\n\x06\x61mount\x18\x04 \x01(\x02\x12\x12\n\nreceiverID\x18\x05 \x01(\x04\x12\x11\n\ttimestamp\x18\x06 \x01(\tb\x06proto3')
)




_TXNPARAM = _descriptor.Descriptor(
  name='txnParam',
  full_name='CMD.txnParam',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='priority', full_name='CMD.txnParam.priority', index=0,
      number=1, type=4, cpp_type=4, label=1,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=18,
  serialized_end=46,
)


_TXNDATA = _descriptor.Descriptor(
  name='txnData',
  full_name='CMD.txnData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='clientID', full_name='CMD.txnData.clientID', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='transactionID', full_name='CMD.txnData.transactionID', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sessionID', full_name='CMD.txnData.sessionID', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='amount', full_name='CMD.txnData.amount', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='receiverID', full_name='CMD.txnData.receiverID', index=4,
      number=5, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='CMD.txnData.timestamp', index=5,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=48,
  serialized_end=172,
)

DESCRIPTOR.message_types_by_name['txnParam'] = _TXNPARAM
DESCRIPTOR.message_types_by_name['txnData'] = _TXNDATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

txnParam = _reflection.GeneratedProtocolMessageType('txnParam', (_message.Message,), dict(
  DESCRIPTOR = _TXNPARAM,
  __module__ = 'txn_pb2'
  # @@protoc_insertion_point(class_scope:CMD.txnParam)
  ))
_sym_db.RegisterMessage(txnParam)

txnData = _reflection.GeneratedProtocolMessageType('txnData', (_message.Message,), dict(
  DESCRIPTOR = _TXNDATA,
  __module__ = 'txn_pb2'
  # @@protoc_insertion_point(class_scope:CMD.txnData)
  ))
_sym_db.RegisterMessage(txnData)


# @@protoc_insertion_point(module_scope)
