"""Test steps for data visualization."""
from mind_monitor.monitor_plot import plot_data

from behave import *

__author__ = 'sb'

from behave import given, when, then


@given('a time series of raw EEG data.')
def step_impl(context):
    context.data_vector = [15, 18, 23, 11, 5, 18]
    context.time_vector = [1414680673.24599,
                           1414680674.24599,
                           1414680675.24599,
                           1414680676.24599,
                           1414680677.24599,
                           1414680678.24599,
                           ]


@given('a time series of theta wave values.')
def step_impl(context):
    context.data_vector = [15, 18, 23, 11, 5, 18]
    context.time_vector = [1414680673.24599,
                           1414680674.24599,
                           1414680675.24599,
                           1414680676.24599,
                           1414680677.24599,
                           1414680678.24599,
                           ]


@when('I plot this data')
def step_impl(context):
    """Create a plot w/o drawing and put it into context for verification."""
    context.figure = plot_data(context.time_vector, context.data_vector)


@then('a line plot is generated.')
def step_impl(context):
    assert context.figure
