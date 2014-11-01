"""Interface to the Mindwave EEG ThinkGear Connector."""

# TODO add license
__author__ = 'sb'

# TODO consider context manager to handle clean-up.

import json
import socket
import logging

PORT = 13854
URL = '127.0.0.1'

logger = logging.getLogger('mind_monitor.interface')


def connect_to_eeg_server(enable_raw_output: bool=False, url: str=URL, port: int=PORT):
    """Connect to ThinkGear Connector.

    :param enable_raw_output: select kind of data to request.
    :param url: the ThinkGear Connector url
    :param port: the ThinkGear Connector port
    :return: socket
    :rtype: socket.socket
    """
    logger.info("Connecting to ThinkGear Connector ...")
    sock_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_.connect((url, port))
    req = {"enableRawOutput": enable_raw_output, "format": "Json"}
    format_req = bytes(json.dumps(req), encoding='iso-8859-1')
    logger.debug("Request: {}".format(repr(format_req)))
    sock_.send(format_req)
    logger.info("Connection to ThinkGear Connector established.")
    return sock_


def clean_raw_data(buf):
    """Clean received data for processing.

    Removes trailing whitespace and splits lines to get single records.

    :param buf: data read from EEG server.
    :type buf: bytes
    :return: separate records as Json strings.
    :rtype: list of str
    """
    raw = str(buf, encoding='iso-8859-1').strip()
    records = raw.splitlines()
    return records


if __name__ == '__main__':
    import log

    log.initialize_logger()
    sock = connect_to_eeg_server()
    sock.close()
