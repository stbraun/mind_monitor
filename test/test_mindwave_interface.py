"""Test accessing data from  ThinkGear connector."""

import json
import socket
import mind_monitor.mindwave_interface as interface
import unittest
import unittest.mock as mock
from genutils.strings import to_bytes

url_port = ('127.0.0.1', 13854)


class TestMindwaveInterface(unittest.TestCase):

    """Test for eeg data access."""

    def setUp(self):
        self.interface = interface.MindWaveInterface()

    def test_connection_and_config_parameters_for_server(self):
        """Test server parameters.

        Checks calls to socket.connect() and socket.send().
        Configuration for enabling and disabling of raw data is tested.
        """
        for enable_raw in [True, False]:
            with self.subTest(enable_raw=enable_raw):
                with mock.patch.object(socket.socket, 'connect', return_value=None) as mock_connect:
                    with mock.patch.object(socket.socket, 'send', return_value=None) as mock_send:
                        self.interface.connect_to_eeg_server(enable_raw)
                mock_connect.assert_called_once_with(url_port)
                args = str(mock_send.call_args[0][0], encoding='iso-8859-1')
                cfg = json.loads(args)
                self.assertIn('enableRawOutput', cfg)
                self.assertEquals(enable_raw, cfg['enableRawOutput'])
                self.assertIn('format', cfg)
                self.assertEquals('Json', cfg['format'])

    def test_handle_record_valid(self):
        """Call handle_record with a valid record."""
        rec = '{"val": 42}'
        data, status, rest = self.interface._handle_record(rec)
        self.assertTrue(status)
        self.assertIsInstance(rest, str)
        self.assertEquals('', rest)
        self.assertIsInstance(data, dict)
        self.assertIn("val", data)
        self.assertEqual(42, data["val"])
        self.assertIn("time", data)

    def test_handle_record_invalid_closing_brace(self):
        """Callhandle_record with an incomplete record."""
        rec = '{"val": {"x": 42, "y": 13}'
        data, status, rest = self.interface._handle_record(rec)
        self.assertFalse(status)
        self.assertEquals(rec, rest)
        # Now call it again with rest and the missing closing brace.
        data, status, rest = self.interface._handle_record(rest + '}')
        self.assertTrue(status)
        self.assertIn('val', data)
        self.assertEqual('', rest)

    def test_handle_record_invalid_no_closing_brace(self):
        """Call handle_record with an incomplete record."""
        rec = '{"val": {"x": 42, "y": 13'
        data, status, rest = self.interface._handle_record(rec)
        self.assertFalse(status)
        self.assertEquals(rec, rest)

    def test_eeg_data_yield(self):
        """Test iterating eeg_data."""
        recs = ['{"val": 0}', '{"val": 1}']
        recs_buf = to_bytes('\n'.join(recs), encoding='ascii')
        with mock.patch.object(socket.socket, 'connect', return_value=None):
            with mock.patch.object(socket.socket, 'send', return_value=None):
                with mock.patch.object(socket.socket, 'recv', return_value=recs_buf) as mock_recv:
                    self.interface = interface.MindWaveInterface()
                    self.interface.connect_to_eeg_server(False)
                    for i, rec in enumerate(self.interface.eeg_data()):
                        if i >= len(recs):
                            assert isinstance(
                                mock_recv, unittest.mock.MagicMock)
                            mock_recv.assert_called_with(1024)
                            return
                        self.assertEqual(i, rec['val'])
