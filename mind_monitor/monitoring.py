"""Monitoring EEG."""

import logging
import sys
import time

import log
from mindwave_interface import connect_to_eeg_server, eeg_data
from monitor_db import connect_to_eeg_db
from monitor_plot import plot_raw_eeg_data

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


def capture_data(eeg, sock, logger, record_raw: bool=False, session_key: str=None):
    """Main loop for data capturing.

    :param eeg: collection for persistence.
    :param sock: socket for communication with MindWave.
    :param record_raw: capture raw data?
    :param session_key: optional session key.
    :param logger: the logger.
    :return: raw, resp. delta data and time data
    :rtype: ([float], [long])
    """
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
    return eeg_data_set, time_data


def main(args):
    """Simple monitoring app.
    :param args: command line parameters.
    :type args: [str]
    """
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
    con, _, session, eeg = connect_to_eeg_db()
    session_key = create_session(session, session_id)
    eeg_data_set, time_data = capture_data(eeg, sock, logger, record_raw, session_key)
    logger.info("Application shutting down ...")
    con.close()
    sock.close()
    logger.info("Shutdown finished.")
    data_in_microvolts = raw_to_micro_volts(eeg_data_set)
    plot_raw_eeg_data(time_data, data_in_microvolts)
    return 0


def raw_to_micro_volts(raw_data_set):
    """Convert a list of raw values to micro volts.

    :param raw_data_set: list of raw values.
    :type raw_data_set: [float]
    :return list of values in micro volts.
    :rtype: [float]
    """
    return [(x * 1.8 / 4096) / 2000 for x in raw_data_set]


if __name__ == '__main__':
    sys.exit(main(sys.argv))
