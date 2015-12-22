"""Monitoring EEG."""

import logging
import sys

from .log import initialize_logger
from .mindwave_interface import MindWaveInterface
from .monitor_plot import plot_raw_eeg_data
from .monitor_sqlite import SQLiteDB

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'


class CaptureData(object):
    """Simple class to work with MindWave."""

    def __init__(self, record_raw=True):
        """Simple monitoring app.

        :param record_raw: optional - True to capture raw data.
        :type record_raw: Bool
        """
        self.logger = logging.getLogger('mind_monitor')
        self.record_raw = record_raw
        self.logger.info("Application started.")
        self.database = SQLiteDB()
        self.mindwave_if = MindWaveInterface()
        self.raw_data_set = []
        self.eeg_data_set = []
        self.time_data = []

    def close(self):
        """Close connections."""
        self.logger.info("Application shutting down ...")
        self.database.close()
        self.mindwave_if.close()
        self.logger.info("Shutdown finished.")

    def plot_raw_data(self):
        """Plot captured raw data."""
        plot_raw_eeg_data(self.time_data, self.raw_data_set)

    def run(self):
        """Start capturing."""
        self.mindwave_if.connect_to_eeg_server(enable_raw_output=self.record_raw)
        self.database.new_session()
        self.capture_data()

    def capture_data(self):
        """Main loop for data capturing."""
        base_time = None
        while True:
            try:
                for json_data in self.mindwave_if.eeg_data():
                    if not base_time:
                        base_time = json_data['time']
                    if self.record_raw and 'rawEeg' in json_data:
                        self.raw_data_set.append(json_data['rawEeg'])
                        self.time_data.append(json_data['time'] - base_time)
                    elif not self.record_raw and 'eegPower' in json_data:
                        self.eeg_data_set.append(json_data['eegPower']['delta'])
                        self.time_data.append(json_data['time'] - base_time)
                    self.database.add_record(json_data)
                    self.logger.debug(json_data)
            except KeyboardInterrupt:
                break
            except Exception as exc:
                self.logger.error("Exception occurred: {}".format(repr(exc)))


def main(args):
    """Simple monitoring app.

    :param args: command line parameters.
    :type args: [str]
    """
    if len(args) > 1:
        record_raw = True
    else:
        record_raw = False
    initialize_logger()
    capture = CaptureData(record_raw=record_raw)
    capture.run()
    capture.close()
    capture.plot_raw_data()


# def raw_to_micro_volts(raw_data_set):
#     """Convert a list of raw values to micro volts.
#
#     :param raw_data_set: list of raw values.
#     :type raw_data_set: [float]
#     :return list of values in micro volts.
#     :rtype: [float]
#     """
#     return [(x * 1.8 / 4096) / 2000 for x in raw_data_set]


if __name__ == '__main__':
    sys.exit(main(sys.argv))
