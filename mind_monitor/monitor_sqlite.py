# coding=utf-8
"""
SQLite implementation.
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

import sqlite3
import time
import os
from .config import DATABASE
from .monitor_common import TIMESTAMP_FORMAT, TRaw, TRecord
from .monitor_dbx import MonitorDB


class SQLiteDB(MonitorDB):
    """SQLite implementation of MonitorDB API."""

    def __init__(self, db=DATABASE):
        """Initialize persistence mechanism.

        :param db: path to database.
        :type db: str
        """
        super().__init__()
        self.db = os.path.expanduser(db)
        self.logger.warning(self.db)
        self.conn = sqlite3.connect(self.db)
        self.setup_db()  # TODO prevent call if DB already there

    def setup_db(self):
        """Setup database schema."""
        cursor = self.conn.cursor()
        # Create tables
        try:
            cursor.execute('''CREATE TABLE sessions ( id INTEGER PRIMARY KEY AUTOINCREMENT,
                              timestamp TEXT,
                              description TEXT)''')
            cursor.execute('''CREATE TABLE comments (
                              session INTEGER REFERENCES "sessions" ("id"),
                              comment TEXT)''')
            cursor.execute('''CREATE TABLE raw_data (
                              session INTEGER REFERENCES "sessions" ("id"),
                              timestamp REAL,
                              data REAL)''')
            cursor.execute('''CREATE TABLE records (
                                session INTEGER REFERENCES "sessions" ("id"), timestamp REAL,
                                highAlpha INT, highBeta INT,  highGamma INT, delta INT, theta INT,
                                lowAlpha INT, lowBeta INT, lowGamma INT,
                                attention INT, meditation INT, poorSignalLevel INT)''')
        except Exception as e:
            self.logger.warning(e)
            pass

    def new_session(self, description=''):
        """Start a new session.

        :param description: optional description of this session
        :type description: str
        """
        super().new_session(description)
        time_stamp = time.strftime(TIMESTAMP_FORMAT)
        self.session_id = self.next_session_id()
        cursor = self.conn.cursor()
        self.logger.info("Creating session: {}".format(self.session_id))
        cursor.execute('''INSERT INTO sessions VALUES (?, ?, ?)''',
                       (self.session_id, time_stamp, description))
        self.conn.commit()

    def next_session_id(self):
        """Determine the next session id."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT max(id) FROM sessions")  # TODO use sequence
        max_id = cursor.fetchone()[0]
        session_id = max_id + 1 if max_id is not None else 0
        return session_id

    def close(self):
        """Close db."""
        self.conn.close()

    def add_comment_to_session(self, comment, session_id=None):
        """Add comment to a session.
        If no session_id is given add to current session.

        :param comment: comment to add
        :type comment: str
        :param session_id: a session id.
        :type session_id: str
        """
        super().add_comment_to_session(comment, session_id)
        if session_id is None:
            session = self.session_id
        else:
            session = session_id
        self.logger.info("Adding comment to session {} - {}.".format(session, comment))
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO comments VALUES(?, ?)''', (session, comment))
        self.conn.commit()

    def add_record(self, record):
        """Add data record to current session.

        :param record: the data record to store.
        """
        # TASK modify interface to expect TRaw / TRecord data type
        super().add_record(record)
        cursor = self.conn.cursor()
        if 'rawEeg' in record:
            cursor.execute('''INSERT INTO raw_data VALUES(?,?,?)''',
                           (self.session_id, record['time'], record['rawEeg']))
        elif 'eegPower' in record:
            cursor.execute('''INSERT INTO records VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                           (self.session_id, record['time'],
                            record['eegPower']['highAlpha'], record['eegPower']['highBeta'],
                            record['eegPower']['highGamma'],
                            record['eegPower']['delta'], record['eegPower']['theta'],
                            record['eegPower']['lowAlpha'], record['eegPower']['lowBeta'],
                            record['eegPower']['lowGamma'],
                            record['eSense']['attention'], record['eSense']['meditation'],
                            record['poorSignalLevel']))
        self.conn.commit()

    def retrieve_session_comments(self, session_id):
        """Retrieve comments stored for session.

        :param session_id: the id of the session.
        :return: comments
        :rtype: [str]
        """
        super().retrieve_session_comments(session_id)
        raise NotImplementedError

    def retrieve_raw_data(self, session_id):
        """Retrieve all raw data records of the session.

        :param session_id: the id of the session
        :return: data records.
        :rtype: [TRaw]
        """
        super().retrieve_data(session_id)
        stmt = 'SELECT * FROM raw_data WHERE "session"=?'
        cursor = self.conn.cursor()
        cursor.execute(stmt, (session_id,))
        raw = map(TRaw._make, cursor.fetchall())
        return list(raw)

    def retrieve_data(self, session_id):
        """Retrieve all data records of the session.

        :param session_id: the id of the session
        :return: data records.
        :rtype: [TRecord]
        """
        super().retrieve_data(session_id)
        cursor = self.conn.cursor()
        stmt = 'select * from records where session=? order by timestamp'
        cursor.execute(stmt, (session_id,))
        records = map(TRecord._make, cursor.fetchall())
        return list(records)
