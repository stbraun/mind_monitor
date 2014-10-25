"""Test accessing data from  ThinkGear connector."""

__author__ = 'sb'

import json
import socket
import mindwave_interface
import unittest
import unittest.mock as mock

url_port = ('127.0.0.1', 13854)


class TestMindwaveInterface(unittest.TestCase):
    """Test for eeg data access."""

    def test_connection_and_config_parameters_for_server(self):
        """Test server parameters.

        Checks calls to socket.connect() and socket.send().
        Configuration for enabling and disabling of raw data is tested.
        """
        for enable_raw in [True, False]:
            with self.subTest(enable_raw=enable_raw):
                with mock.patch.object(socket.socket, 'connect', return_value=None) as mock_connect:
                    with mock.patch.object(socket.socket, 'send', return_value=None) as mock_send:
                        mindwave_interface.connect_to_eeg_server(enable_raw)
                mock_connect.assert_called_once_with(url_port)
                args = str(mock_send.call_args[0][0], encoding='iso-8859-1')
                cfg = json.loads(args)
                self.assertIn('enableRawOutput', cfg)
                self.assertEquals(enable_raw, cfg['enableRawOutput'])
                self.assertIn('format', cfg)
                self.assertEquals('Json', cfg['format'])
