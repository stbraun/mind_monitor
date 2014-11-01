"""Test steps for data visualization."""
__author__ = 'sb'

from behave import given, when, then


@given('a time series of raw EEG data.')
def step_impl(context):
    context.given = 'blue'
    pass

@when('I plot this data')
def step_impl(context):
    """Create a plot w/o drawing and put it into context for verification."""
    plt = None
    context.plot = plt
    pass


@then('a line plot is generated.')
def step_impl(context):
    #assert context.plot
    pass