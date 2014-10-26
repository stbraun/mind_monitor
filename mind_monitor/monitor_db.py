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
    :return: connection, database, and collection collection
    :rtype: (MongoClient, db, collection)
    """
    logger.info("Connecting to MongoDB ...")
    con = pymongo.MongoClient()
    db = con.eeg_db
    collection = db.eeg
    logger.info("Connected and db opened.")
    return con, db, collection
