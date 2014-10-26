"""Test logging configuration."""
import logging
import logging.config
import log

__author__ = 'sb'

import unittest


class TestLoggingConfiguration(unittest.TestCase):
    """Test case for configuration of logging."""

    def test_initialize_logger(self):
        log.initialize_logger()
        logger = logging.getLogger('mind_monitor')
        self.assertTrue(logger.isEnabledFor(logging.DEBUG))
        self.assertFalse(logger.propagate)
