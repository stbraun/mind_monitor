"""Explore Interface.

Get some data to get a feel for it and see some results.
"""
from mindwave_interface import connect_to_eeg_server, clean_raw_data
from monitor_mongo import connect_to_eeg_db
from monitor_plot import plot_raw_eeg_data

__author__ = 'sb'

import sys
import time

import json
import logging

logger = logging.getLogger('exploreinterface')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(ch)


def read_raw_data_from_server():
    """Read raw data stream from server."""
    s = connect_to_eeg_server(enable_raw_output=True)
    loop = 50
    while loop > 0:
        buf = s.recv(1024)
        raw = str(buf).strip()
        print(raw)
        loop -= 1
    s.close()


def read_json_from_server():
    """Read stream from server."""
    s = connect_to_eeg_server(enable_raw_output=True)
    loop = 50
    while loop > 0:
        loop -= 1
        buf = s.recv(1024)
        records = clean_raw_data(buf)
        for record in records:
            jres = json.loads(record)
            print(repr(jres))
    s.close()


def act_on_blink():
    """Print blinks."""
    s = connect_to_eeg_server()
    logger.info("Start receiving ...")
    while True:
        buf = s.recv(1024)
        raw = str(buf, encoding='iso-8859-1').strip()
        try:
            jres = json.loads(raw)
            if 'blinkStrength' in jres:
                bs = jres['blinkStrength']
                logger.info("Blink strength; {}".format(repr(bs)))
                if bs > 100:
                    print("That's too much blinking!")
                    break
                if bs > 70:
                    print("You're blinking!")
        except ValueError as ve:
            logger.error('Exception occurred: {}'.format(repr(ve)))
    s.close()


def store_eeg_in_mongodb(eeg_data):
    """Store EEG data in mongo db."""
    con, eeg = connect_to_eeg_db()
    for eeg_record in eeg_data:
        eeg.insert(eeg_record)
    con.close()


def list_eeg_data():
    con, eeg = connect_to_eeg_db()
    records = eeg.find()
    for record in records:
        print(record)
    con.close()


def clear_eeg_db():
    con, eeg = connect_to_eeg_db()
    records = eeg.find()
    for record in records:
        eeg.remove(record)
    con.close()

## -----------------------------------------------------------------------


def main(argv):
    logger.info("Application started.")
    sock = connect_to_eeg_server(enable_raw_output=True)
    con, db, session, eeg = connect_to_eeg_db()
    raw_eeg_data = []
    time_data = []
    base_time = None
    while True:
        try:
            buf = sock.recv(1024)
            records = clean_raw_data(buf)
            for record in records:
                jres = json.loads(record)
                jres['time'] = time.time()
                print(repr(jres))
                try:
                    raw_eeg_data.append(jres['rawEeg'])
                    if not base_time:
                        base_time = jres['time']
                    time_data.append(jres['time'] - base_time)
                except KeyError:
                    pass
                eeg.insert(jres)
        except KeyboardInterrupt:
            break
        except Exception as exc:
            logger.error("Exception occurred: {}".format(repr(exc)))
    logger.info("Application shutting down ...")
    con.close()
    sock.close()
    logger.info("Shutdown finished.")
    plot_raw_eeg_data(time_data, raw_eeg_data)
    return 0

if __name__ == '__main__':
    # read_raw_data_from_server()
    # read_json_from_server()
    # act_on_blink()
    # read_and_decode_stream()
    sys.exit(main(sys.argv))


# { "_id" : ObjectId("54427615bc32e79f81ae4bbc"), "rawEeg" : -92 }
# { "_id" : ObjectId("54427615bc32e79f81ae4bbd"), "rawEeg" : -54 }
# { "_id" : ObjectId("54427615bc32e79f81ae4bbe"), "rawEeg" : 59 }
# { "_id" : ObjectId("54427615bc32e79f81ae4bbf"), "eSense" : { "meditation" : 75, "attention" : 54 }, "poorSignalLevel" : 0, "eegPower" : { "delta" : 874006, "lowGamma" : 3197, "theta" : 53351, "lowBeta" : 6113, "highBeta" : 9367, "lowAlpha" : 36106, "highGamma" : 27478, "highAlpha" : 9544 } }

# > db.eeg.find({'eegPower.delta' : {'$gt' : 1000000}}, {'eegPower.delta' : 1})
# { "_id" : ObjectId("54427613bc32e79f81ae47bb"), "eegPower" : { "delta" : 1361089 } }
# { "_id" : ObjectId("54427614bc32e79f81ae49bd"), "eegPower" : { "delta" : 1103412 } }
# { "_id" : ObjectId("54427756bc32e79f9f3ebd49"), "eegPower" : { "delta" : 1290018 } }
# { "_id" : ObjectId("54427757bc32e79f9f3ebf4a"), "eegPower" : { "delta" : 1719340 } }
# { "_id" : ObjectId("54427758bc32e79f9f3ec147"), "eegPower" : { "delta" : 1101799 } }
