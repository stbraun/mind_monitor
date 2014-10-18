"""Explore Interface.

Get some data to get a feel for it and see some results.
"""
__author__ = 'sb'

import sys
import time
import pymongo
import matplotlib.pyplot as plt

import socket
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
        records = cleanup_raw_data(buf)
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

def connect_to_eeg_server(enable_raw_output: bool=False):
    """Connect to Mindwave server.
    :param enable_raw_output: select kind of data to request.
    :return: socket
    :rtype: socket.socket
    """
    logger.info("Connecting to EEG server ...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 13854))
    req = {"enableRawOutput": enable_raw_output, "format": "Json"}
    format_req = bytes(json.dumps(req), encoding='iso-8859-1')
    logger.debug("Request: {}".format(repr(format_req)))
    s.send(format_req)
    logger.info("Connection to EEG server established.")
    return s


def cleanup_raw_data(buf):
    """Clean received data for processing.
    :param buf: data read from EEG server.
    :type buf: bytes
    :return: separate records
    :rtype: list of str
    """
    raw = str(buf, encoding='iso-8859-1').strip()
    records = raw.splitlines()
    return records


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


def plot_raw_eeg_data(data):
    """Plot data as line plot.

    :param data: values to plot.
    :type: [float]
    """
    plt.plot(data, enumerate(data)[0], 'b.')
    # plt.xlim(min(x_data) - 1, max(x_data) + 1)
    # plt.ylim(min(y_data) - 1, max(y_data) + 1)
    plt.show()

def main(argv):
    logger.info("Application started.")
    sock = connect_to_eeg_server(enable_raw_output=True)
    con, db, eeg = connect_to_eeg_db()
    raw_eeg_data = []
    while True:
        try:
            buf = sock.recv(1024)
            records = cleanup_raw_data(buf)
            for record in records:
                jres = json.loads(record)
                jres['time'] = time.time()
                print(repr(jres))
                try:
                    raw_eeg_data.append(jres['raeEeg'])
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
    plot_raw_eeg_data(raw_eeg_data)
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

# def plot_diff_top_tables(self):
#     """Plot the difference of table growth."""
#     fig = plt.figure(figsize=(16, 12))
#     # rows
#     fig_rows = fig.add_subplot(2, 1, 1)
#     plt.subplots_adjust(hspace=0, left=0.2, right=0.95, bottom=0)
#     sorted_by_rows = self.diff.sort(columns=DIFF_ROW_COUNT, ascending=False)
#     rows = pd.Series(sorted_by_rows[DIFF_ROW_COUNT])
#     rows.index = sorted_by_rows[TABLE_NAME]
#     title = 'Diff rows numbers: {}'.format(self.meaning)
#     plt.xlabel('diff rows created per device')
#     plt.ylabel('table name')
#     rows[-20:].plot(kind='barh', title=title, ax=fig_rows)
#     plt.text(plt.xlim()[0], plt.ylim()[1]+0.1, "Sum: {:6.0f}".format(rows.sum()))
#     # sizes
#     fig_sizes = fig.add_subplot(2, 1, 2)
#     plt.subplots_adjust(hspace=0.15, left=0.2, right=0.95, bottom=0.05, top=0.95)
#     sorted_by_size = self.diff.sort(columns=DIFF_SIZE_KB, ascending=False)
#     sizes = pd.Series(sorted_by_size[DIFF_SIZE_KB])
#     sizes.index = sorted_by_size[TABLE_NAME]
#     title = 'Diff table sizes: {}'.format(self.meaning)
#     plt.xlabel('Diff growth in KB per device')
#     plt.ylabel('table name')
#     sizes[-20:].plot(kind='barh', title=title, ax=fig_sizes)
#     plt.text(plt.xlim()[0], plt.ylim()[1]+0.1, "Sum: {:4.1f}".format(sizes.sum()))
#     #
#     if self.screen:
#         plt.show()
#     else:
#         file_name = '_'.join(self.meaning.split()) + '_growth_diff.png'
#         pth = os.path.join(self.target_path_figures, file_name)
#         plt.savefig(pth)
#     plt.close()
