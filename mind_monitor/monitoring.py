"""Monitoring EEG."""

# TODO add licencse
import json
import logging
import sys
import time

import log
from mindwave_interface import connect_to_eeg_server, cleanup_raw_data
from monitor_db import connect_to_eeg_db
from monitor_plot import plot_raw_eeg_data

# TODO remove logic from main()
BUFFER_SIZE = 1024
MAX_QUALITY_LEVEL = 200
POOR_SIGNAL_LEVEL = 'poorSignalLevel'


def create_session(collection, id: str=None, description: str=''):
    time_stamp = time.strftime('%Y-%m-%d %H:%M:%S')
    if id is None:
        id = time_stamp
    session = {'key': id, 'description': description, 'timestamp': time_stamp}
    collection.insert(session)
    return id


def main(args):
    """Simple monitoring app."""
    # TODO improve argument handling.
    if len(args) > 1:
        session_id = args[1]
    else:
        session_id = None
    log.initialize_logger()
    logger = logging.getLogger('mindwave')
    logger.info("Application started.")
    sock = connect_to_eeg_server(enable_raw_output=True)
    con, db, session, eeg = connect_to_eeg_db()
    session_key = create_session(session, session_id)
    raw_eeg_data = []
    time_data = []
    base_time = None
    while True:
        try:
            buf = sock.recv(BUFFER_SIZE)
            records = cleanup_raw_data(buf)
            for record in records:
                jres = json.loads(record)
                if POOR_SIGNAL_LEVEL in jres and jres[POOR_SIGNAL_LEVEL] >= MAX_QUALITY_LEVEL:
                    # ignore bad data
                    logger.warning("Bad signal quality: {}".format(repr(jres[POOR_SIGNAL_LEVEL])))
                    continue
                jres['time'] = time.time()
                jres['session'] = session_key
                logger.info(jres)
                try:
                    raw_eeg_data.append(jres['rawEeg'])
                    if not base_time:
                        base_time = jres['time']
                    time_data.append(jres['time'] - base_time)
                except KeyError:
                    pass
                eeg.insert(jres)
                logger.info(".")
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
    sys.exit(main(sys.argv))
