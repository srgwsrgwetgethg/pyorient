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

try:
    import configparser
except ImportError:
    import ConfigParser as configparser


def get_test_config():
    # Read test configuration from the file 'tests.cfg'
    config = configparser.RawConfigParser()
    config.read('./tests/tests.cfg')

    # getfloat(), getint() and getboolean() raise an exceptions if the value is not of the specific type
    return {
        'host': config.get('server', 'host'),
        'port': config.get('server', 'port'),
        'can_root': config.getboolean('server', 'can_root'),
        'root_username': config.get('root', 'user'),
        'root_password': config.get('root', 'pwd'),
        'user_username': config.get('user', 'user'),
        'user_password': config.get('user', 'pwd'),
        'existing_db': config.get('db', 'existing'),
        'new_db': config.get('db', 'new')
    }
