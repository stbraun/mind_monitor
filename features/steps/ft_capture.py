"""Test steps for capturing pre-processed EEG data."""
import logging

from behave import *

__author__ = 'sb'

import json
import socket
from unittest import mock
from mind_monitor.mindwave_interface import MindWaveInterface
from behave import given, when, then

RETURN_VALUE = b'{ "eSense" : { "meditation" : 75, "attention" : 54 }, "poorSignalLevel" : 0, "eegPower" : { "delta" : 874006, "lowGamma" : 3197, "theta" : 53351, "lowBeta" : 6113, "highBeta" : 9367, "lowAlpha" : 36106, "highGamma" : 27478, "highAlpha" : 9544 } }'

logger = logging.getLogger('mind_monitor.interface')


def connect_via_mock(enable_raw: bool):
    """Connect via mock.
    :param enable_raw: True to request raw data.
    :return: mocks for connect and send.
    """
    mw = MindWaveInterface()
    with mock.patch.object(socket.socket, 'connect', return_value=None) as mock_connect:
        with mock.patch.object(socket.socket, 'send', return_value=None) as mock_send:
            with mock.patch.object(socket.socket, 'recv', return_value=RETURN_VALUE) as mock_recv:
                sock = mw.connect_to_eeg_server(enable_raw_output=enable_raw)
                for rr in mw.eeg_data():
                    logger.info("--> {} : {}".format(type(rr), rr))
                    break
    return sock, mock_connect, mock_send, mock_recv, rr


@when('I select pre-processed data')
def step_impl(context):
    """We want to disable raw data and only store waves."""
    sock, m_con, m_send, m_recv, data = connect_via_mock(False)
    context.sock = sock
    context.m_con = m_con
    context.m_send = m_send
    context.m_recv = m_recv
    context.data = data
    context.raw = False
    context.waves = True
    logger.info("When - Read: {}".format(data))

@when('I start a measurement')
def step_impl(context):
    """Start a new session and read some records."""
    #context.data = []
    # with mock.patch.object(socket.socket, 'recv', return_value=RETURN_VALUE) as mock_recv:
    #     record = eeg_data(context.sock)
    logger.info("When2 - context.data: {}".format(context.data))
    #context.data.append(data)
    context.m_recv.assert_called_once()


def assert_raw_mode(context):
    """Check that raw mode is set as expected."""
    args = str(context.m_send.call_args[0][0], encoding='iso-8859-1')
    cfg = json.loads(args)
    assert 'enableRawOutput' in cfg
    assert context.raw == cfg['enableRawOutput']


@then('pre-processed data is captured.')
def step_impl(context):
    """Verify the data."""
    context.m_con.assert_called_once()
    context.m_send.assert_called_once()
    assert_raw_mode(context)

    assert len(context.data) > 0
    record = context.data
    from pprint import pprint as pp
    pp(record)
    assert 'eegPower' in record