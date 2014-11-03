"""Monitoring EEG."""

# TODO add licencse
import json
import logging
import sys
import time

import log
from mindwave_interface import connect_to_eeg_server, clean_raw_data, eeg_data
from monitor_db import connect_to_eeg_db
from monitor_plot import plot_raw_eeg_data

# TODO remove logic from main()
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'


def create_session(collection, session_id: str=None, description: str=''):
    """Create a new session.

    If given, session_id will be the session session_id. Otherwise a timestamp will be used
    to identify the session.
    :param collection: the collection to store the session record.
    :param session_id: (optional) session id.
    :param description: (optional) description of session.
    :return: the session session_id
    :rtype: str
    """
    time_stamp = time.strftime(TIMESTAMP_FORMAT)
    if session_id is None:
        session_id = time_stamp
    session = {'key': session_id, 'description': description, 'timestamp': time_stamp}
    collection.insert(session)
    return session_id


def main(args):
    """Simple monitoring app.
    :param args: command line parameters.
    :type args: [str]
    """
    # TODO improve argument handling.
    if len(args) > 1:
        session_id = args[1]
    else:
        session_id = None
    if len(args) > 2:
        record_raw = True
    else:
        record_raw = False
    log.initialize_logger()
    logger = logging.getLogger('mindwave')
    logger.info("Application started.")
    sock = connect_to_eeg_server(enable_raw_output=record_raw)
    con, db, session, eeg = connect_to_eeg_db()
    session_key = create_session(session, session_id)
    eeg_data_set = []
    time_data = []
    base_time = None
    while True:
        try:
            for jres in eeg_data(sock):
                jres['session'] = session_key
                if record_raw:
                    try:
                        eeg_data_set.append(jres['rawEeg'])
                        if not base_time:
                            base_time = jres['time']
                        time_data.append(jres['time'] - base_time)
                    except KeyError:
                        pass
                else:
                    if 'eegPower' in jres:
                        eeg_data_set.append(jres['eegPower']['delta'])
                        if not base_time:
                            base_time = jres['time']
                        time_data.append(jres['time'] - base_time)
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
    plot_raw_eeg_data(time_data, eeg_data_set) # record_raw)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
