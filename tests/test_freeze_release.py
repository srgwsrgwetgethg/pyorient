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


class FreezeReleaseTestCase(unittest.TestCase):

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
            client.db_close()
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


