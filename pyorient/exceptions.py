__author__ = 'Ostico <ostico@gmail.com>, Marc Auberer <marc.auberer@sap.com>'

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


class PyOrientException(Exception):
    def __init__(self, class_name, errors):
        # Get the class name of the raised exception
        _errorClass = class_name.split(".")[-1]

        exceptions = {
            "OCommandSQLParsingException": PyOrientSQLParsingException,
            "ODatabaseException": PyOrientDatabaseException,
            "OConfigurationException": PyOrientDatabaseException,
            "OCommandExecutorNotFoundException": PyOrientCommandException,
            "OSecurityAccessException": PyOrientSecurityAccessException,
            "ORecordDuplicatedException": PyOrientORecordDuplicatedException,
            "OSchemaException": PyOrientSchemaException,
            "OIndexException": PyOrientIndexException
        }

        # Override generic PyOrientException type by searching in the exception map
        if _errorClass in exceptions.keys():
            self.__class__ = exceptions[_errorClass]

        # Initialize exception
        Exception.__init__(self, class_name)
        self.errors = errors

    def __str__(self):
        # Print error message
        if self.errors:
            return "%s - %s" % (Exception.__str__(self), self.errors[0])
        else:
            return Exception.__str__(self)


class PyOrientConnectionException(PyOrientException):
    pass


class PyOrientConnectionPoolException(PyOrientException):
    pass


class PyOrientSecurityAccessException(PyOrientException):
    pass


class PyOrientDatabaseException(PyOrientException):
    pass


class PyOrientSQLParsingException(PyOrientException):
    pass


class PyOrientCommandException(PyOrientException):
    pass


class PyOrientSchemaException(PyOrientException):
    pass


class PyOrientIndexException(PyOrientException):
    pass


class PyOrientORecordDuplicatedException(PyOrientException):
    pass


class PyOrientBadMethodCallException(PyOrientException):
    pass


class PyOrientWrongProtocolVersionException(PyOrientException):
    pass


class PyOrientInvalidSerializationModeException(PyOrientException):
    pass


class PyOrientSerializationException(PyOrientException):
    pass


class PyOrientNullRecordException(PyOrientException):
    pass
