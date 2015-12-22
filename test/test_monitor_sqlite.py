# coding=utf-8
"""
Test SQLite interface.
"""
# Copyright (c) 2015 Stefan Braun
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE
# AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import unittest
import os

from mind_monitor.monitor_sqlite import SQLiteDB


class TestSQLiteDB(unittest.TestCase):
    """Test case for persistence using SQLite.."""

    def setUp(self):
        # Create test database
        self.DATABASE = "test.db"
        self.db = SQLiteDB(db=self.DATABASE)
        self.db.setup_db()

    def tearDown(self):
        # Delete test database
        if os.path.exists(self.DATABASE):
            os.remove(self.DATABASE)

    def test_next_session(self):
        self.assertEqual(0, self.db.next_session_id(), 'First session id shall be 0.')
        self.db.new_session()
        self.assertEqual(0, self.db.session_id, 'Next session id shall be incremented.')
        self.assertEqual(1, self.db.next_session_id(), 'Next session id shall be incremented.')

    def test_add_raw_record(self):
        self.db.new_session()
        sid = self.db.session_id
        rec = {'time': 12345, 'rawEeg': 42}
        self.db.add_record(rec)
        data = self.db.retrieve_raw_data(sid)
        self.assertEqual(1, len(data), 'One record found.')
        self.assertEqual(3, len(data[0]), 'Three values found.')
        record = data[0]
        self.assertEqual(3, len(record))
        self.assertEqual(0, record.session)
        self.assertEqual(42, record.data)
        self.assertEqual(12345, record.timestamp)
