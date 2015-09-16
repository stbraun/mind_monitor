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
from monitor_dbx import MonitorDB

DATABASE = '/Users/sb/.eeg.db'
# TODO use centralized format for timestamps
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'


class SQLiteDB(MonitorDB):
    """SQLite implementation of MonitorDB API."""

    def __init__(self, logger):
        """Initialize persistence mechanism.
        :param logger: the logger.
        """
        super().__init__(logger)
        self.conn = sqlite3.connect(DATABASE)
        self.setup_db()

    def setup_db(self):
        """Setup database schema."""
        cursor = self.conn.cursor()
        # Create tables
        try:
            cursor.execute('''CREATE TABLE sessions (id TEXT, timestamp TEXT, description TEXT)''')
            cursor.execute('''CREATE TABLE comments (session TEXT, comment TEXT)''')
            cursor.execute('''CREATE TABLE raw_data (session TEXT, timestamp TEXT, data REAL)''')
            cursor.execute('''CREATE TABLE records (session TEXT, timestamp TEXT,
                                highAlpha INT, highBeta INT,  highGamma INT, delta INT, theta INT,
                                lowAlpha INT, lowBeta INT, lowGamma INT,
                                attention INT, meditation, poorSignalLevel INT)''')
        except:
            pass

    def new_session(self, description=''):
        """Start a new session.

        :param description: optional description of this session
        :type description: str
        """
        super().new_session(description)
        time_stamp = time.strftime(TIMESTAMP_FORMAT)
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO sessions VALUES (?, ?, ?)''',
                       (self.session_id, time_stamp, description))
        self.conn.commit()

    def close(self):
        """Close db."""
        self.conn.close()

    def add_comment_to_session(self, comment, session_id=''):
        """Add comment to a session.
        If no session_id is given add to current session.

        :param comment: comment to add
        :type comment: str
        :param session_id: a session id.
        :type session_id: str
        """
        super().add_comment_to_session(comment, session_id)
        if session_id == '':
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
        return []

    def retrieve_data(self, session_id):
        """Retrieve all records of the session.
        :param session_id: the id of the session
        :return: data records.
        :rtype: [{}]
        """
        super().retrieve_data(session_id)
        raise NotImplementedError
        return []
