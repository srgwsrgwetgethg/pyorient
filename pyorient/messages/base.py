#  Copyright 2020 Niko Usai <usai.niko@gmail.com>, http://mogui.it; Marc Auberer, https://marc-auberer.de
#
#  this file is part of pyorient
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#   limitations under the License.

__author__ = 'mogui <mogui83@gmail.com>, Marc Auberer <marc.auberer@sap.com>'

import struct
import sys

from ..exceptions import PyOrientBadMethodCallException, PyOrientCommandException, PyOrientNullRecordException
from ..utils import is_debug_active
from ..orient import OrientSocket
from ..serializations import OrientSerialization
from ..constants import FIELD_INT, FIELD_STRING, INT, STRING, STRINGS, BYTE, BYTES, BOOLEAN, SHORT, LONG
from ..hexdump import hexdump

# Initialize global variable
in_transaction = False


class BaseMessage(object):
    def __init__(self, sock=OrientSocket):
        """
        :type sock: OrientSocket
        """
        # Initialize attributes
        sock.get_connection()
        self._orientSocket = sock
        self._protocol = self._orientSocket.protocol
        self._session_id = self._orientSocket.session_id
        self._auth_token = self._orientSocket.auth_token
        self._request_token = False

        self._header = []
        self._body = []
        self._fields_definition = []

        self.command = chr(0)
        self._db_opened = self._orientSocket.db_opened
        self._connected = self._orientSocket.connected

        self._node_list = []
        self._serializer = None
        self._output_buffer = b''
        self._input_buffer = b''

        # Callback method for async queries
        self._callback = None
        # Callback method for push notifications from the server
        self._push_callback = None

        self._need_token = True

        global in_transaction

    def get_serializer(self):
        """
        Lazy return of the serialization, we retrieve the type from the :class: `OrientSocket
        <pyorient.orient.OrientSocket> object`
        :return: an instance of the serializer, suitable for encoding and decoding
        """
        props = None
        if self._orientSocket.serialization_type == OrientSerialization.Binary:
            props = self._orientSocket.props
        return OrientSerialization.get_impl(OrientSerialization.Binary, props)

    def get_orient_socket_instance(self):
        """
        Return of the current instance of :class: `OrientSocket <pyorient.orient.OrientSocket>`
        """
        return self._orientSocket

    def is_connected(self):
        """
        Return boolean, if socket is connected
        """
        return self._connected

    def database_opened(self):
        """
        Return boolean, if a database is open
        """
        return self._db_opened

    def get_cluster_map(self):
        """
        :type: list of [OrientNode]
        """
        return self._node_list

    def set_session_token(self, token=''):
        """
        :param token: Set the request to True to use the token authentication
        :type token: bool|string
        :return: self
        """
        if token != '' and token is not None:
            if type(token) is bool:
                self._request_token = token
            elif type(token) is str or type(token) is bytes:
                self._request_token = True
                self._auth_token = token
                self._db_opened = True
                self._connected = True
                self._update_socket_token()
        return self

    def get_session_token(self):
        pass

    def _update_socket_id(self):
        pass

    def _update_socket_token(self):
        pass

    def _reset_fields_definition(self):
        pass

    def prepare(self, *args):
        # Session id
        self._fields_definition.insert(1, (FIELD_INT, self._session_id))

        # Auth token
        if self._need_token and self._request_token is True:
            self._fields_definition.insert(2, (FIELD_STRING, self._auth_token))

        # Build output buffer
        self._output_buffer = b''.join(self._encode_field(x) for x in self._fields_definition)
        return self

    def get_protocol(self):
        if self._protocol < 0:
            self._protocol = self._orientSocket.protocol
        return self._protocol

    def _decode_header(self):
        pass

    def _decode_body(self):
        pass

    def _decode_all(self):
        pass

    def fetch_response(self, *_continue):
        """
        Decode header and body
        if flag 'continue' is set, read only body because header has already been read
        :param _continue:
        :return:
        """
        if len(_continue) != 0:
            self._body = []
            self._decode_body()
            self.dump_streams()
            # already fetched, get last results as cache info
        elif len(self._body) == 0:
            self._decode_all()
            self.dump_streams()
        return self._body

    def dump_streams(self):
        if is_debug_active():
            # Dump streams, when debug mode is enabled
            if len(self._output_buffer):
                print("\nRequest :")
                hexdump(self._output_buffer)
                # print(repr(self._output_buffer))
            if len(self._input_buffer):
                print("\nResponse:")
                hexdump(self._input_buffer)
                # print(repr(self._input_buffer))

    def _append(self, field):
        """
        @:rtype self: BaseMessage
        @type field: object
        """
        self._fields_definition.append(field)
        return self

    def __str__(self):
        pass

    def send(self):
        if self._orientSocket.in_transaction is False:
            self._orientSocket.write(self._output_buffer)
            self._reset_fields_definition()
        if is_debug_active():
            self.dump_streams()
            # Reset output buffer
            self._output_buffer = b''
        return self

    def close(self):
        self._orientSocket.close()

    @staticmethod
    def _encode_field(field):
        # tuple with type
        t, v = field
        _content = None

        if t['type'] == INT:
            _content = struct.pack("!i", v)
        elif t['type'] == SHORT:
            _content = struct.pack("!h", v)
        elif t['type'] == LONG:
            _content = struct.pack("!q", v)
        elif t['type'] == BOOLEAN:
            _content = bytes([1]) if v else bytes([0])
        elif t['type'] == BYTE:
            _content = bytes([ord(v)])
        elif t['type'] == BYTES:
            _content = struct.pack("!i", len(v)) + v
        elif t['type'] == STRING:
            if isinstance(v, str):
                v = v.encode('utf-8')
            _content = struct.pack("!i", len(v)) + v
        elif t['type'] == STRINGS:
            _content = b''
            for s in v:
                if isinstance(s, str):
                    s = s.encode('utf-8')
                _content += struct.pack("!i", len(s)) + s

        return _content

    def _decode_field(self, _type):
        pass

    def _read_async_records(self):
        pass

    def _read_record(self):
        pass
