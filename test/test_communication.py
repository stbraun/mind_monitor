"""Test the communication with mindwave device via sockets"""
__author__ = 'sb'

import unittest
import logging
import time
import socket


class TestCommunication(unittest.TestCase):
    """Explore and test communication with mindwave device."""

    def setUp(self):
        """Connect to the mindwave server."""
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.assertIsInstance(self.s, socket.socket)
        self.s.connect(('127.0.0.1', 13854))

    def tearDown(self):
        self.s.close()

    def test_switch_to_json(self):
        """Request Json format."""
        format_req = b'{"enableRawOutput": true, "format": "Json"}'
        res = self.s.send(format_req)
        logging.log(logging.WARN, 'sent format request ...')
        self.assertEqual(res, len(format_req))
        buf = self.s.recv(1024)
        self.assertIsNotNone(buf)
        data = str(buf)
        self.assertIsInstance(data, str)
        logging.log(logging.WARN, 'received: {}'.format(repr(data)))
        time.sleep(10)
        buf = self.s.recv(1024)
        self.assertIsNotNone(buf)
        data = str(buf)
        self.assertIsInstance(data, str)
        time.sleep(10)
