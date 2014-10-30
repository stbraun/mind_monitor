"""Test steps for session support."""
from unittest import mock
import time
from mind_monitor.monitoring import create_session
from pymongo import MongoClient
from pymongo.database import Database, Collection

__author__ = 'sb'

from behave import given, when, then

ID = 'test_id'


@given('system is set up.')
def step_impl(context):
    pass

@when('I start a measurement')
def step_impl(context):
    """Actually just create a session."""
    with mock.patch.object(Collection, 'insert', return_value=None) as mock_collection:
        context.id = create_session(Collection(Database(MongoClient(), 'blub'), 'eeg'))
    context.coll =  mock_collection.assert_called_once()

@then('all data points captured will be accessible as one set.')
def step_impl(context):
    """Simply check id."""
    assert(time.strptime(context.id, '%Y-%m-%d %H:%M:%S'))
    context.coll.assert_called_once()


@when('starting measurements I enter a session id.')
def step_impl(context):
    """Actually just create a session."""
    collection = Collection(Database(MongoClient(), 'blub'), 'eeg')
    with mock.patch.object(Collection, 'insert', return_value=None) as mock_collection:
        context.id = create_session(collection, id=ID)
    context.coll =  mock_collection.assert_called_once()

@then('all data points captured in this can be accessed using this session id.')
def step_impl(context):
    assert(context.id == ID)
    context.coll.assert_called_once()
