import unittest
import os
import sys
import pyorient

os.environ['DEBUG'] = "1"
os.environ['DEBUG_VERBOSE'] = "0"
# if os.path.realpath('../') not in sys.path:
#     sys.path.insert(0, os.path.realpath('../'))
#
# if os.path.realpath('.') not in sys.path:
#     sys.path.insert(0, os.path.realpath('.'))

import pyorient
from uuid import uuid4
from pyorient.constants import DB_TYPE_DOCUMENT
from pyorient.orient import OrientSocket
from pyorient.messages.database import ConnectMessage, DbFreezeMessage, DbReleaseMessage, DbOpenMessage


class FreezeReleaseTestCase(unittest.TestCase):

    def connect(self):

        connection = OrientSocket("localhost", 2424)
        conn_msg = ConnectMessage(connection)

        print("%r" % conn_msg.get_protocol())
        assert conn_msg.get_protocol() != -1

        session_id = conn_msg.prepare(("root", "root")) \
            .send().fetch_response()

        print("Sid: %s" % session_id)
        assert session_id == connection.session_id
        assert session_id != -1
        # ##################

        msg = DbOpenMessage(connection)

        db_name = "test_freeze_and_release_db"
        cluster_info = msg.prepare(
            (db_name, "root", "root", DB_TYPE_DOCUMENT, "")
        ).send().fetch_response()

        assert len(cluster_info) != 0

        return connection, cluster_info

    def test_fandr(self):
        conn, info = self.connect()

        msg = DbFreezeMessage(conn)
        msg.prepare().send()

        msg = DbReleaseMessage(conn)
        msg.prepare().send()

    def test_freeze_and_release(self):

        client = pyorient.OrientDB("localhost", 2424)
        session_id = client.connect("root", "root")
        db_name = "test_freeze_and_release_db"
        if not client.db_exists(db_name):
            client.db_create(db_name)

        client.db_open(db_name, "root", "root")

        client.command("CREATE CLASS TestClass IF NOT EXISTS")
        client.command("INSERT INTO TestClass (id, name) VALUES ('{id}', '{name}')".format(id = str(uuid4()), name="maakt_niet_uit"))

        try:
            client.db_freeze()
            #client.db_close()
            
        except RuntimeError as re:
            pass
        
        # this should throw an error
        # client.command("INSERT INTO TestClass (id, name) VALUES ('{id}', '{name}')".format(id = str(uuid4()), name="maakt_niet_uit"))

        client = pyorient.OrientDB("localhost", 2424)
        session_id = client.connect("root", "root")
       
        client.db_open(db_name, "root", "root")
        client.db_release()

        # this should run without error
        client.command("INSERT INTO TestClass (id, name) VALUES ('{id}', '{name}')".format(id = str(uuid4()), name="maakt_niet_uit"))




