"""Database for monitoring data."""
import pymongo
import logging
__author__ = 'sb'


logger = logging.getLogger('mindwave.db')


def connect_to_eeg_db():
    """Connect to database.

    Connects to a local MongoDB server and opens 'eeg_db' database.
    If the database does not exist yet, it will be created.
    :return: connection, database, and collection eeg
    :rtype: (MongoClient, db, collection)
    """
    logger.info("Connecting to MongoDB ...")
    con = pymongo.MongoClient()
    db = con.eeg_db
    eeg = db.eeg
    logger.info("Connected and db opened.")
    return con, db, eeg
