"""Test steps for capturing pre-processed EEG data."""
__author__ = 'sb'

import json
import socket
from unittest import mock
from mind_monitor import mindwave_interface

RETURN_VALUE = '{ "_id" : ObjectId("54427615bc32e79f81ae4bbf"), "eSense" : { "meditation" : 75, "attention" : 54 }, "poorSignalLevel" : 0, "eegPower" : { "delta" : 874006, "lowGamma" : 3197, "theta" : 53351, "lowBeta" : 6113, "highBeta" : 9367, "lowAlpha" : 36106, "highGamma" : 27478, "highAlpha" : 9544 } }'


from behave import given, when, then


def connect_via_mock(enable_raw: bool):
    """Connect via mock.
    :param enable_raw: True to request raw data.
    :return: mocks for connect and send.
    """
    with mock.patch.object(socket.socket, 'connect', return_value=None) as mock_connect:
        with mock.patch.object(socket.socket, 'send', return_value=None) as mock_send:
            with mock.patch.object(socket.socket, 'receive', return_value=("%s" % RETURN_VALUE)) as mock_rcv:
                mindwave_interface.connect_to_eeg_server(enable_raw)
    return mock_connect, mock_send


@when('I select pre-processed data')
def step_impl(context):
    """We want to disable raw data and only store waves."""
    m_con, m_send = connect_via_mock(False)
    context.m_con = m_con
    context.m_send = m_send
    context.raw = False
    context.waves = True

@when('I start a measurement')
def step_impl(context):
    """Start a new session and read some records."""
    context.data = []


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