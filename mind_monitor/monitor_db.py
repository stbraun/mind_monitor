"""Database for monitoring data."""
import pymongo
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
    :rtype: (MongoClient, db, c_session, c_eeg)
    """
    logger.info("Connecting to MongoDB ...")
    con = pymongo.MongoClient()
    db = con.eeg_db
    c_eeg = db.eeg
    c_session = db.session
    logger.info("Connected and db opened.")
    return con, db, c_session, c_eeg
