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
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
import json
import logging
import threading

from genutils.strings import to_bytes

from .config import PORT_RECORDS, MINDWAVE_URL, MINDWAVE_PORT
from .publish import publish
from .mindwave_interface import MindWaveInterface, is_bad_quality
from .monitor_sqlite import SQLiteDB


class CaptureEEGData(threading.Thread):
    """Simple class to work with MindWave."""

    def __init__(self, record_raw=True):
        """Simple monitoring app.
        :param record_raw: optional - True to capture raw data.
        :type record_raw: Bool
        """
        threading.Thread.__init__(self, name='CaptureEEGData')
        self.logger = logging.getLogger('mind_monitor.capture')
        self.record_raw = record_raw
        self.logger.info("Application started.")
        self.database = None
        self.mindwave_if = None
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
        self.database = SQLiteDB()  # TASK - move database related stuff out of this class
        self.mindwave_if = MindWaveInterface()
        self.mindwave_if.connect_to_eeg_server(
                enable_raw_output=self.record_raw, url=MINDWAVE_URL, port=MINDWAVE_PORT)
        self.database.new_session()  # TASK - move database stuff
        with publish(PORT_RECORDS)as pub:
            while True:
                try:
                    for json_data in self.mindwave_if.eeg_data():
                        self.logger.debug(json_data)
                        if not is_bad_quality(json_data):
                            if self.record_raw and self.__is_raw_data(json_data):
                                pub.send_multipart([b'raw', to_bytes(json.dumps(json_data))])
                            elif self.__is_power_data(json_data):
                                pub.send_multipart([b'power', to_bytes(json.dumps(json_data))])
                            self.database.add_record(json_data)  # TASK - move database stuff
                        if self.__stop:
                            self.__close()
                            return
                except Exception as exc:
                    self.logger.error('Exception occurred: {}'.format(repr(exc)))
                    break

    @staticmethod
    def __is_raw_data(record):
        """Determine if record contains raw data."""
        return 'rawEeg' in record

    @staticmethod
    def __is_power_data(record):
        """Determine if record contains power data."""
        return 'eegPower' in record
