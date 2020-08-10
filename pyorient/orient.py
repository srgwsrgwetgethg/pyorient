__author__ = 'mogui <mogui83@gmail.com>, Marc Auberer <marc.auberer@sap.com>'

# Python imports
import socket
import struct

# Local imports
from .serializations import OrientSerialization
from .utils import dlog
from .constants import SOCK_CONN_TIMEOUT, FIELD_SHORT, SUPPORTED_PROTOCOL, ERROR_ON_NEWER_PROTOCOL
from .exceptions import PyOrientConnectionPoolException, PyOrientWrongProtocolVersionException, PyOrientConnectionException

class OrientSocket(object):
    """
    Class representing the binary connection to the database, it does all the low level communication and holds information on server version and cluster map
    .. DANGER:: Should not be used directly
    :param host: hostname of the server to connect
    :param port: integer port of the server
    """
    def __init__(self, host, port, serialization_type=OrientSerialization.CSV):
        # Initialize attributes with default values
        self.connected = False
        self.host = host
        self.port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.protocol = -1
        self.session_id = -1
        self.db_opened = None
        self.serialization_type = serialization_type
        self.in_transaction = False
        self._props = None

    def get_connection(self):
        # Establish the socket connection and return the connected socket
        if not self.connected:
            self.connect()
        return self._socket

    def connect(self):
        """
        Connects to the database server
        could raise :class:`PyOrientConnectionPoolException`
        """
        dlog("Trying to connect ...")
        try:
            # Set timeout and connect socket to the provided host and port
            self._socket.settimeout(SOCK_CONN_TIMEOUT)
            self._socket.connect((self.host, self.port))

            # Read short value from server to check, if the server is working correctly
            _answer = self._socket.recv(FIELD_SHORT['bytes'])
            if len(_answer) != 2:  # A short is 2 bytes long
                # Close the socket and throw exception if the server is not working correctly
                self._socket.close()
                raise PyOrientConnectionPoolException("Server sent empty string", [])

            # Unpack protocol version
            self.protocol = struct.unpack('!h', _answer)[0]

            # Raise exception on higher protocol version than supported, if enabled
            if self.protocol > SUPPORTED_PROTOCOL and ERROR_ON_NEWER_PROTOCOL:
                raise PyOrientWrongProtocolVersionException("Protocol version " + str(self.protocol) + " is not "
                      "supported by this client version. Please check, if there's a new pyorient version available", [])

            self.connected = True
        except socket.error as e:
            # Catch the exception and raise it up as a PyOrientConnectionException
            self.connected = False
            raise PyOrientConnectionException("Socket error: %s" % e, [])

    def close(self):
        """
        Close the connection to the database server
        """
        # Stop connection
        self._socket.close()
        self.connected = False
        # Reset all attributes to default
        self.host = ''
        self.port = 0
        self.protocol = -1
        self.session_id = -1

    def write(self, buff):
        pass
