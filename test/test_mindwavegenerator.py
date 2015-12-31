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

from mindwavegenerator import gen_power_record, gen_poor_signal, gen_blink_event, gen_mental_effort, \
    gen_familiarity


class TestMindWaveGenerator(unittest.TestCase):
    def test_gen_poor_signal(self):
        record = gen_poor_signal()
        self.assertIsInstance(record, bytes)
        data = json.loads(to_str(record))
        self.assertEqual(200, data['poorSignalLevel'])

    def test_gen_power_record(self):
        record = gen_power_record()
        self.assertIsInstance(record, bytes)
        data = json.loads(to_str(record))
        self.assertLessEqual(data['poorSignalLevel'], 50)

    def test_gen_blink_event(self):
        record = gen_blink_event()
        self.assertIsInstance(record, bytes)
        data = json.loads(to_str(record))
        self.assertIn('blinkStrength', data)
        self.assertLessEqual(data['blinkStrength'], 100)

    def test_gen_familiarity(self):
        record = gen_familiarity()
        self.assertIsInstance(record, bytes)
        data = json.loads(to_str(record))
        self.assertIn('familiarity', data)
        self.assertEqual(float, type(data['familiarity']))

    def test_gen_mental_effort(self):
        record = gen_mental_effort()
        self.assertIsInstance(record, bytes)
        data = json.loads(to_str(record))
        self.assertIn('mentalEffort', data)
        self.assertEqual(float, type(data['mentalEffort']))
