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
def main(args):
    """Simple monitoring app."""
    log.initialize_logger()
    logger = logging.getLogger('mindwave')
    logger.info("Application started.")
    sock = connect_to_eeg_server(enable_raw_output=True)
    con, db, eeg = connect_to_eeg_db()
    raw_eeg_data = []
    time_data = []
    base_time = None
    while True:
        try:
            buf = sock.recv(1024)
            records = cleanup_raw_data(buf)
            for record in records:
                jres = json.loads(record)
                jres['time'] = time.time()
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
    sys.exit(main(sys.argv))
