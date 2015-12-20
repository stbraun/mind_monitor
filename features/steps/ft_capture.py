"""Test steps for capturing pre-processed EEG data."""
import logging

from behave import *

__author__ = 'sb'

RETURN_VALUE = b'{ "eSense" : { "meditation" : 75, "attention" : 54 }, "poorSignalLevel" : 0, "eegPower" : { "delta" : 874006, "lowGamma" : 3197, "theta" : 53351, "lowBeta" : 6113, "highBeta" : 9367, "lowAlpha" : 36106, "highGamma" : 27478, "highAlpha" : 9544 } }'

logger = logging.getLogger('mind_monitor.interface')


@when('I select pre-processed data')
def step_impl(context):
    """We want to disable raw data and only store waves."""
    raise NotImplementedError


@when('I start a measurement')
def step_impl(context):
    """Start a new session and read some records."""
    raise NotImplementedError


@then('pre-processed data is captured.')
def step_impl(context):
    """Verify the data."""
    raise NotImplementedError
