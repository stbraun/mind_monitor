"""Database for monitoring data."""
from pymongo import MongoClient
from pymongo.database import Database, Collection
import logging
__author__ = 'sb'

# TODO
# A couple of assumptions were made:
#  * local mongo server
#  * database name
#  * collection name
#
# *At least* document these assumptions.
# *Better:* make them explicit and overridable.

logger = logging.getLogger('mind_monitor.db')


def connect_to_eeg_db():
    """Connect to database.

    Connects to a local MongoDB server and opens 'eeg_db' database.
    If the database does not exist yet, it will be created.
    :return: connection, database, c_session and c_eeg.
    :rtype: (MongoClient, Database, Collection, Collection)
    """
    logger.info("Connecting to MongoDB ...")
    con = MongoClient()
    db = con.eeg_db
    assert isinstance(db, Database)
    c_eeg = db.eeg
    c_session = db.session
    logger.info("Connected and db opened.")
    assert isinstance(c_session, Collection)
    assert isinstance(c_eeg, Collection)
    return con, db, c_session, c_eeg
