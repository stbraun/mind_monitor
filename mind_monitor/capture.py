# coding=utf-8
"""
Capture EEG data.
"""
# Copyright (c) 2015 Stefan Braun
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE
# AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import logging
from time import sleep
from mindwave_interface import MindWaveInterface
from monitor_sqlite import SQLiteDB
import threading


class CaptureEEGData(threading.Thread):
    """Simple class to work with MindWave."""

    def __init__(self, record_raw=True):
        """Simple monitoring app.
        :param record_raw: optional - True to capture raw data.
        :type record_raw: Bool
        """
        threading.Thread.__init__(self, name='CaptureEEGData')
        self.logger = logging.getLogger('mind_monitor')
        self.record_raw = record_raw
        self.logger.info("Application started.")
        self.database = None
        self.mindwave_if = None
        self.raw_data_set = []
        self.eeg_data_set = []
        self.time_data = []
        self.__stop = False

    def __close(self):
        """Close connections."""
        self.logger.info("Closing connections ...")
        self.database.close()
        self.mindwave_if.close()
        self.logger.info("Connections closed.")

    def start(self):
        """Start capturing."""
        self.__stop = False
        super().start()

    def stop(self):
        """Stop capturing data."""
        self.__stop = True

    def run(self):
        """Main loop for data capturing."""
        self.logger.info('Starting capture thread...')
        base_time = None
        self.database = SQLiteDB()
        self.mindwave_if = MindWaveInterface()
        self.mindwave_if.connect_to_eeg_server(enable_raw_output=self.record_raw)
        self.database.new_session()
        while True:
            try:
                for json_data in self.mindwave_if.eeg_data():
                    if not self.__is_bad_quality(json_data):
                        if not base_time:
                            base_time = json_data['time']
                        if self.record_raw and self.__is_raw_data(json_data):
                            self.raw_data_set.append(json_data['rawEeg'])
                            self.time_data.append(json_data['time'] - base_time)
                        elif not self.record_raw and self.__is_power_data(json_data):
                            self.eeg_data_set.append(json_data['eegPower']['delta'])
                            self.time_data.append(json_data['time'] - base_time)
                        self.database.add_record(json_data)
                        self.logger.debug(json_data)
                    if self.__stop:
                        self.__close()
                        return
            except Exception as exc:
                self.logger.error('Exception occurred: {}'.format(repr(exc)))

    def __is_raw_data(self, record):
        """Determine if record contains raw data."""
        return 'rawEeg' in record

    def __is_power_data(self, record):
        """Determine if record contains power data."""
        return 'eegPower' in record

    def __is_bad_quality(self, record):
        """Determine if record contains bad quality data."""
        return 'quality' in record and record['quality'] == 'BAD'

