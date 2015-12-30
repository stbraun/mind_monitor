# coding=utf-8
"""
A generator for simulated mindwave records.
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


# msg_bad_quality = b'{"poorSignalLevel": 200}\n'
# msg_good_quality = b'{"eSense" : { "meditation" : 75, "attention" : 54 }, ' \
#                    b'"poorSignalLevel" : 0, ' \
#                    b'"eegPower" : { "delta" : 874006, "lowGamma" : 3197, "theta" : 53351, ' \
#                    b'"lowBeta" : 6113, "highBeta" : 9367, "lowAlpha" : 36106, ' \
#                    b'"highGamma" : 27478, "highAlpha" : 9544 } }\n'

import json
import random

from genutils.strings import to_bytes


class MindWaveGenerator:
    def gen_poor_signal(self):
        """Generate a poor signal record."""
        return b'{"poorSignalLevel": 200}'

    def gen_power_record(self):
        """Generate a record with randomized power data."""
        record = {"eSense": {"meditation": self._rnd_percent(), "attention": self._rnd_percent()},
                  "poorSignalLevel": self._rnd_int(upper=50),
                  "eegPower": {"delta": self._rnd_int(upper=150000),
                               "lowGamma": self._rnd_int(upper=150000),
                               "theta": self._rnd_int(upper=150000),
                               "lowBeta": self._rnd_int(upper=150000),
                               "highBeta": self._rnd_int(upper=150000),
                               "lowAlpha": self._rnd_int(upper=150000),
                               "highGamma": self._rnd_int(upper=150000),
                               "highAlpha": self._rnd_int(upper=150000)}}
        return to_bytes(json.dumps(record))

    def gen_raw_record(self):
        """Generate a raw EEG record."""
        record = {"rawEeg": self._rnd_int(lower=-2000, upper=2000)}
        return to_bytes(json.dumps(record))

    def gen_blink_event(self):
        """Generate a blinking event."""
        record = {"blinkStrength": self._rnd_percent()}
        return to_bytes(json.dumps(record))

    def gen_familiarity(self):
        """Generate a familiarity event."""
        record = {"familiarity": self._rnd_float()}
        return to_bytes(json.dumps(record))

    def gen_mental_effort(self):
        """Generate a mental effort event."""
        record = {"mentalEffort": self._rnd_float()}
        return to_bytes(json.dumps(record))

    def _rnd_percent(self):
        return self._rnd_int()

    def _rnd_int(self, lower=0, upper=100):
        return random.randint(lower, upper)

    def _rnd_float(self, lower=0, upper=100):
        return random.uniform(lower, upper)