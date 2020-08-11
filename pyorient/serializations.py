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

from .exceptions import PyOrientBadMethodCallException, PyOrientInvalidSerializationModeException
from pyorient.serializer import *

# Try to import pyorient_native. The binary protocol only can be used only pyorient_native is available
try:
    import pyorient_native
    binary_can_be_used = True
except ImportError:
    binary_can_be_used = False


class OrientSerialization(object):
    """
    Enumeration of all available serialization modes. Default: CSV
    """
    CSV = "ORecordDocument2csv"
    Binary = "ORecordSerializerBinary"
    impl_map = {
        CSV: OrientSerializationCSV,
        Binary: OrientSerializationBinary
    }

    @classmethod
    def get_impl(cls, impl, props=None):
        # Select class based on the passed serialization mode
        implementation = cls.impl_map.get(impl, False)
        if not implementation:
            # Raise an exception when something invalid gets passed to the get_impl method
            raise PyOrientBadMethodCallException(impl + ' is not an available serialization type', [])
        elif impl == cls.Binary and not binary_can_be_used:
            # Raise an exception when binary mode is selected, but pyorient_native is not installed
            raise PyOrientInvalidSerializationModeException(impl + ' cannot be used,'
                  'when pyorient_native library is not installed.')
        elif impl == cls.Binary:
            # Binary mode was selected and pyorient_native is available
            return implementation(props)
        else:
            # CSV mode was selected
            return implementation()
