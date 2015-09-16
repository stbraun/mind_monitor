"""Monitoring EEG."""

import logging
import sys
import time

import log
from mindwave_interface import connect_to_eeg_server, eeg_data
from monitor_plot import plot_raw_eeg_data
from monitor_sqlite import SQLiteDB

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

database = None


def create_session(session_id: str=None, description: str=''):
    """Create a new session.

    If given, session_id will be the session session_id. Otherwise a timestamp will be used
    to identify the session.
    :param session_id: (optional) session id.
    :param description: (optional) description of session.
    :return: session
    :rtype: {'key', 'description', 'timestamp'}
    """
    time_stamp = time.strftime(TIMESTAMP_FORMAT)
    if session_id is None:
        session_id = time_stamp
    session = {'key': session_id, 'description': description, 'timestamp': time_stamp}
    return session


def capture_data(sock, logger, record_raw=False):
    """Main loop for data capturing.

    :param sock: socket for communication with MindWave.
    :param record_raw: capture raw data?
    :type record_raw: bool
    :param logger: the logger.
    :return: raw, resp. delta data and time data
    :rtype: ([float], [long])
    """
    global database
    eeg_data_set = []
    time_data = []
    base_time = None
    while True:
        try:
            for jres in eeg_data(sock):
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
                database.add_record(jres)
                logger.info(jres)
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
    global database
    if len(args) > 1:
        record_raw = True
    else:
        record_raw = False
    log.initialize_logger()
    logger = logging.getLogger('mind_monitor')
    logger.info("Application started.")
    sock = connect_to_eeg_server(enable_raw_output=record_raw)
    database = SQLiteDB(logger)
    database.new_session()
    eeg_data_set, time_data = capture_data(sock, logger, record_raw)
    logger.info("Application shutting down ...")
    database.close()
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
