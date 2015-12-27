# coding=utf-8
"""
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

import unittest
import json

from genutils.strings import to_str

from mindwavegenerator import MindWaveGenerator


class TestMindWaveGenerator(unittest.TestCase):
    def setUp(self):
        self.gen = MindWaveGenerator()

    def test_gen_poor_signaä(self):
        record = self.gen.gen_poor_signal()
        self.assertIsInstance(record, bytes)
        data = json.loads(to_str(record))
        self.assertEqual(200, data['poorSignalLevel'])

    def test_gen_power_record(self):
        record = self.gen.gen_power_record()
        self.assertIsInstance(record, bytes)
        data = json.loads(to_str(record))
        self.assertLessEqual(data['poorSignalLevel'], 50)
