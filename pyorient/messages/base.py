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

    def set_session_token(self):
        pass

    def get_session_token(self):
        pass

    def _update_socket_id(self):
        pass

    def _update_socket_token(self):
        pass

    def _reset_fields_definition(self):
        pass

    def prepare(self, *args):
        pass

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
        if len(_continue) is not 0:
            self._body = []
            self._decode_body()
            self.dump_streams()
            # already fetched, get last results as cache info
        elif len(self._body) is 0:
            self._decode_all()
            self.dump_streams()
        return self._body

    def dump_streams(self):
        if is_debug_active():
            # Dump streams, when debug mode is enabled
            if len(self._output_buffer):
                print("\nRequest :")
                #hexdump(self._output_buffer)
                # print(repr(self._output_buffer))
            if len(self._input_buffer):
                print("\nResponse:")
                #hexdump(self._input_buffer)
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
        pass

    def _decode_field(self, _type):
        pass

    def _read_async_records(self):
        pass

    def _read_record(self):
        pass
