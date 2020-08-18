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

import unittest
import pyorient


class OrientVersionTestCase(unittest.TestCase):
    """ Orient Version Test Case """

    @staticmethod
    def test_string2():
        release = "1.10.1"
        x = pyorient.OrientVersion(release)
        assert isinstance(x.major, int)
        assert isinstance(x.minor, int)
        assert isinstance(x.build, int)
        assert x.major == 1
        assert x.minor == 10
        assert x.build == 1
        assert x.subversion == ''

    @staticmethod
    def test_string3():
        release = "2.0.19-rc2"
        x = pyorient.OrientVersion(release)
        assert isinstance(x.major, int)
        assert isinstance(x.minor, int)
        assert isinstance(x.build, int)
        assert isinstance(x.subversion, str)
        assert x.major == 2
        assert x.minor == 0
        assert x.build == 19
        assert x.subversion == "rc2"

    @staticmethod
    def test_string4():
        release = "2.2.0 ;Unknown (build 0)"
        x = pyorient.OrientVersion(release)
        assert isinstance(x.major, int)
        assert isinstance(x.minor, int)
        assert isinstance(x.build, int)
        assert isinstance(x.subversion, str)
        assert x.major == 2
        assert x.minor == 2
        assert x.build == 0
        assert x.subversion == ";Unknown (build 0)"

    @staticmethod
    def test_string5():
        release = "2.2-rc1 ;Unknown (build 0)"
        x = pyorient.OrientVersion(release)
        assert isinstance(x.major, int)
        assert isinstance(x.minor, int)
        assert isinstance(x.build, int)
        assert isinstance(x.subversion, str)
        assert x.major == 2
        assert x.minor == 2
        assert x.build == 0
        assert x.subversion == "rc1 ;Unknown (build 0)"

    @staticmethod
    def test_string6():
        release = "v2.2"
        x = pyorient.OrientVersion(release)
        assert isinstance(x.major, int)
        assert isinstance(x.minor, int)
        assert isinstance(x.build, int)
        assert isinstance(x.subversion, str)
        assert x.major == 2
        assert x.minor == 2
        assert x.build == 0
        assert x.subversion == ""

    @staticmethod
    def test_string_version2():
        release = "2.2.0 (build develop@r79d281140b01c0bc3b566a46a64f1573cb359783; 2016-05-18 14:14:32+0000)"
        x = pyorient.OrientVersion(release)
        assert isinstance(x.major, int)
        assert isinstance(x.minor, int)
        assert isinstance(x.build, int)
        assert isinstance(x.subversion, str)
        assert x.major == 2
        assert x.minor == 2
        assert x.build == 0
        assert x.subversion == "(build develop@r79d281140b01c0bc3b566a46a64f1573cb359783; 2016-05-18 14:14:32+0000)"

    @staticmethod
    def test_new_string():
        release = "OrientDB Server v2.2.0 (build develop@r79d281140b01c0bc3b566a46a64f1573cb359783; 2016-05-18 14:14:32+0000)"
        x = pyorient.OrientVersion(release)
        assert isinstance(x.major, int)
        assert isinstance(x.minor, int)
        assert isinstance(x.build, int)
        assert isinstance(x.subversion, str)
        assert x.major == 2
        assert x.minor == 2
        assert x.build == 0
        assert x.subversion == "(build develop@r79d281140b01c0bc3b566a46a64f1573cb359783; 2016-05-18 14:14:32+0000)"


if __name__ == '__main__':
    unittest.main()
