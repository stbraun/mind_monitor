# coding=utf-8
"""
Abstract class describing interface of persistence mechanism.
"""
# Copyright (c) 2015 Stefan Braun
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE
# AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import logging

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'


class MonitorDB(object):
    """Abstract persistence class."""
    def __init__(self):
        """Initialize persistence mechanism.
        """
        super().__init__()
        self.logger = logging.getLogger('mind_monitor.db')

        self.logger.info("Initializing MonitorDB")
        self.session_id = None
        self.description = ''
        pass

    def new_session(self, description=''):
        """Start a new session.

        :param description: optional description of this session
        :type description: str
        """
        self.description = description

    def close(self):
        """Close db."""
        pass

    def add_comment_to_session(self, comment, session_id=None):
        """Add comment to a session.
        If no session_id is given add to current session.

        :param comment: comment to add
        :type comment: str
        :param session_id: optional session id.
        :type session_id: str
        """
        pass

    def add_record(self, record):
        """Add data record to current session.
        :param record: the data record to store.
        """
        self.logger.info("Adding data record to session: {} - {}.".format(self.session_id, record))
        pass

    def retrieve_session_comments(self, session_id):
        """Retrieve comments stored for session.
        :param session_id: the id of the session.
        :return: comments
        :rtype: [str]
        """
        self.logger.info("Retrieve comments for session: {}.".format(session_id))
        return []

    def retrieve_raw_data(self, session_id):
        """Retrieve all raw data records of the session.
        :param session_id: the id of the session
        :return: data records.
        :rtype: [{}]
        """
        self.logger.info("Retrieve raw data for session: {}.".format(session_id))
        return []

    def retrieve_data(self, session_id):
        """Retrieve all records of the session.
        :param session_id: the id of the session
        :return: data records.
        :rtype: [{}]
        """
        self.logger.info("Retrieve data for session: {}.".format(session_id))
        return []
