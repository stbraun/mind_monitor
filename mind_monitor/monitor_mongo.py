"""Database for monitoring data."""
from pymongo import MongoClient
from pymongo.database import Database, Collection
import logging
import time
from monitor_dbx import MonitorDB

__author__ = 'sb'

# TODO
# A couple of assumptions were made:
#  * local MongoDB server
#  * database name
#  * collection name
#
# *At least* document these assumptions.
# *Better:* make them explicit and customizable.

# TODO use centralized format for timestamps
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'


class MongoDB(MonitorDB):
    """MongoDB implementation."""

    def __init__(self, logger):
        super().__init__(logger)
        self.con = None
        self.db = None
        self.c_session = None
        self.c_eeg = None
        # init db and set attributes
        self.connect_to_eeg_db()

    def connect_to_eeg_db(self):
        """Connect to database.

        Connects to a local MongoDB server and opens 'eeg_db' database.
        If the database does not exist yet, it will be created.
        :return: connection, database, c_session and c_eeg.
        :rtype: (MongoClient, Database, Collection, Collection)
        """
        self.logger.info("Connecting to MongoDB ...")
        self.con = MongoClient()
        self.db = self.con.eeg_db
        assert isinstance(self.db, Database)
        self.c_eeg = self.db.eeg
        self.c_session = self.db.session
        self.logger.info("Connected and db opened.")
        assert isinstance(self.c_session, Collection)
        assert isinstance(self.c_eeg, Collection)

    def new_session(self, description=''):
        """Start a new session.

        :param description: optional description of this session
        :type description: str
        """
        super().new_session(session_id)
        time_stamp = time.strftime(TIMESTAMP_FORMAT)
        session = {'key': self.session_id, 'description': self.description, 'timestamp': time_stamp}
        self.c_session.insert_one(session)

    def add_comment_to_session(self, comment, session_id=''):
        """Add comment to a session.
        If no session_id is given add to current session.

        :param comment: comment to add
        :type comment: str
        :param session_id: a session id.
        :type session_id: str
        """
        self.logger.info("Adding comment is NOT SUPPORTED")

    def add_record(self, record):
        """Add data record to current session.
        :param record: the data record to store.
        """
        super().add_record(record)
        record['session'] = self.session_id
        self.c_eeg.insert_one(record)
