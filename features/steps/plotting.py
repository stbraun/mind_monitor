"""Test steps for data visualization."""
__author__ = 'sb'

from behave import given, when, then
import behave


@given('a time series of raw EEG data.')
def step_impl(context):
    pass

@when('I plot this data')
def step_impl(context):
    pass


@then('a line plot is generated.')
def step_impl(context):
    assert
