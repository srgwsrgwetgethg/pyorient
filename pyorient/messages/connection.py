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

from ..constants import CONNECT_OP, FIELD_BYTE, FIELD_INT, FIELD_SHORT, FIELD_STRINGS, FIELD_BOOLEAN, FIELD_STRING,\
    NAME, SUPPORTED_PROTOCOL, VERSION, SHUTDOWN_OP
from ..exceptions import PyOrientBadMethodCallException
from ..utils import need_connected
from .base import BaseMessage


class ConnectMessage(BaseMessage):
    pass
