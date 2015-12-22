"""Interface to the Mindwave EEG ThinkGear Connector."""

import time
import json
import socket
import logging

from genutils.strings import to_bytes, to_str

PORT = 13854
URL = '127.0.0.1'
BUFFER_SIZE = 1024
MAX_QUALITY_LEVEL = 200
POOR_SIGNAL_LEVEL = 'poorSignalLevel'


class MindWaveInterface(object):

    """Interface to MindWave headset."""

    def __init__(self):
        self.logger = logging.getLogger('mind_monitor.interface')
        self.sock_ = None
        self.raw_data = False
        self.bad_quality = False

    def connect_to_eeg_server(self, enable_raw_output=False, url=URL, port=PORT):
        """Connect to ThinkGear Connector.

        :param enable_raw_output: select kind of data to request.
        :param url: the ThinkGear Connector url
        :param port: the ThinkGear Connector port
        """
        self.logger.info("Connecting to ThinkGear Connector ...")
        self.raw_data = enable_raw_output
        self.sock_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_.connect((url, port))
        req = {"enableRawOutput": enable_raw_output, "format": "Json"}
        format_req = to_bytes(json.dumps(req), encoding='ascii')
        self.logger.debug("Request: {}".format(repr(format_req)))
        self.sock_.send(format_req)
        self.logger.info("Connection to ThinkGear Connector established.")

    def eeg_data(self):
        """Retrieve eeg data and provide it a record per call.
        Yields one record per call.
        """
        # TASK yield data as TRaw / TRecord / TQuality
        rest = ''
        while True:
            buf = to_bytes(rest, encoding='ascii') + self.sock_.recv(BUFFER_SIZE)
            raw = to_str(buf, encoding='ascii').strip()
            for record in raw.splitlines():
                data, status, rest = self._handle_record(record)
                if status:
                    yield data

    def _handle_record(self, record):
        """Handle a single record.

        :param record: record as string
        :type record: str
        :return: (data, status, rest)
        :rtype: (dict, boolean, str)
        """
        rest = ''
        try:
            data = json.loads(record, encoding="utf-8")
        except json.JSONDecodeError:
            # handle incomplete records
            return None, False, record
        # TASK pull out bad data handling to improve clarity
        if POOR_SIGNAL_LEVEL in data and data[POOR_SIGNAL_LEVEL] >= MAX_QUALITY_LEVEL:
            # ignore bad data
            if not self.bad_quality:
                self.logger.warning(
                    "Bad signal quality: {}".format(repr(data[POOR_SIGNAL_LEVEL])))
                self.bad_quality = True
            return {'quality': 'BAD'}, True, rest
        if self.bad_quality:
            self.bad_quality = False
            self.logger.warning("Signal quality recovered.")
        data['time'] = time.time()
        self.logger.info(' yielding {}'.format(data))
        return data, True, rest

    def close(self):
        """Close connection."""
        self.sock_.close()
