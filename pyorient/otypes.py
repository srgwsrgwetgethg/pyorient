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

import re


class OrientVersion(object):
    def __init__(self, release):
        """
        Object representing Orient db release Version
        :param release: String release
        """
        self.release = release  # Full version string of OrientDB release
        self.major = None  # Mayor version
        self.minor = None  # Minor version
        self.build = None  # Build number
        self.subversion = None   # Build version string
        self.parse_version(release)

    def parse_version(self, release_string):
        # Convert release string to string object
        if not isinstance(release_string, str):
            release_string = release_string.decode()

        # Split '.'
        try:
            version_info = release_string.split(".")
            self.major = version_info[0]
            self.minor = version_info[1]
            self.build = version_info[2]
        except IndexError:
            pass

        # Validate major version
        regex = re.match('.*([0-9]+).*', self.major)
        self.major = regex.group(1)

        # Split '-'
        try:
            version_info = self.minor.split("-")
            self.minor = version_info[0]
            self.subversion = version_info[1]
        except IndexError:
            pass

        # Validate build number and subversion
        try:
            regex = re.match('([0-9]+)[\.\- ]*(.*)', self.build)
            self.build = regex.group(1)
            self.subversion = regex.group(2)
        except TypeError:
            pass

        # Convert numbers to ints and version strings to strings
        self.major = int(self.major)
        self.minor = int(self.minor)
        self.build = 0 if self.build is None else int(self.build)
        self.subversion = '' if self.subversion is None else str(self.subversion)
