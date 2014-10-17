"""Explore Interface.

Get some data to get a feel for it and see some results.
"""
__author__ = 'sb'

import socket
import json
import logging

logger = logging.getLogger('exploreinterface')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(ch)


def read_from_server():
    """Read stream from server."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 13854))
    format_req = b'{"enableRawOutput": true, "format": "Json"}'
    s.send(format_req)
    loop = 50
    while loop > 0:
        buf = s.recv(1024)
        raw = str(buf).strip()
        print(raw)
        loop -= 1
    s.close()


def read_json_from_server():
    """Read stream from server."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 13854))
    format_req = b'{"enableRawOutput": false, "format": "Json"}'
    s.send(format_req)
    loop = 50
    while loop > 0:
        buf = s.recv(1024)
        raw = str(buf, encoding='iso-8859-1').strip()
        jres = json.loads(raw)
        print(repr(jres))
        loop -= 1
    s.close()


def act_on_blink():
    """Print blinks."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 13854))
    format_req = b'{"enableRawOutput": false, "format": "Json"}'
    s.send(format_req)
    logger.info("Start receiving ...")
    while True:
        buf = s.recv(1024)
        raw = str(buf, encoding='iso-8859-1').strip()
        try:
            jres = json.loads(raw)
            if 'blinkStrength' in jres:
                bs = jres['blinkStrength']
                logger.info("Blink strength; {}".format(repr(bs)))
                if bs > 100:
                    print("That's too much blinking!")
                    break
                if bs > 70:
                    print("You're blinking!")
        except ValueError as ve:
            logger.error('Exception occurred: {}'.format(repr(ve)))
    s.close()


if __name__ == '__main__':
    # read_from_server()
    read_json_from_server()
    # act_on_blink()
