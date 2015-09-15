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

import time

TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'


class MonitorDB(object):
    """Abstract persistence class."""
    def __init__(self, logger):
        """Initialize persistence mechanism.
        :param logger: the logger.
        """
        super().__init__()
        self.logger = logger
        self.logger.info("Initializing MonitorDB")
        self.new_session()
        pass

    def new_session(self, session_id=''):
        """Start a new session.
        If no session_id is given a timestamp is used.

        :param session_id: the identifier of this session.
        :type session_id: str
        """
        if session_id == '':
            self.session_id = time.strftime(TIMESTAMP_FORMAT)
        else:
            self.session_id = session_id
        self.logger.info("Creating session: {}".format(self.session_id))
        pass

    def add_comment_to_session(self, comment, session_id=''):
        """Add comment to a session.
        If no session_id is given add to current session.

        :param comment: comment to add
        :type comment: str
        :param session_id: a session id.
        :type session_id: str
        """
        if session_id == '':
            session = self.session_id
        else:
            session = session_id
        self.logger.info("Adding comment to session {} - {}.".format(session, comment))
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

    def retrieve_data(self, session_id):
        """Retrieve all records of the session.
        :param session_id: the id of the session
        :return: data records.
        :rtype: [{}]
        """
        self.logger.info("Retrieve data for session: {}.".format(session_id))
        return []
