# coding=utf-8
"""
A generator for simulated mindwave records.
"""

# Copyright (c) 2015 Stefan Braun
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and
# associated documentation files (the "Software"), to deal in the Software
# without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to
# whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE
# AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
#  LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import json
import random

from genutils.strings import to_bytes


def _rnd_int(lower=0, upper=100):
    return random.randint(lower, upper)


def _rnd_float(lower=0, upper=100):
    return random.uniform(lower, upper)


def _rnd_percent():
    return _rnd_int()


def gen_poor_signal():
    """Generate a poor signal record."""
    return b'{"poorSignalLevel": 200}'


def gen_power_record():
    """Generate a record with randomized power data."""
    record = {
        "eSense": {"meditation": _rnd_percent(), "attention": _rnd_percent()},
        "poorSignalLevel": _rnd_int(upper=50),
        "eegPower": {"delta": _rnd_int(upper=150000),
                     "lowGamma": _rnd_int(upper=150000),
                     "theta": _rnd_int(upper=150000),
                     "lowBeta": _rnd_int(upper=150000),
                     "highBeta": _rnd_int(upper=150000),
                     "lowAlpha": _rnd_int(upper=150000),
                     "highGamma": _rnd_int(upper=150000),
                     "highAlpha": _rnd_int(upper=150000)}}
    return to_bytes(json.dumps(record))


def gen_raw_record():
    """Generate a raw EEG record."""
    record = {"rawEeg": _rnd_int(lower=-2048, upper=2047)}
    return to_bytes(json.dumps(record))


def gen_blink_event():
    """Generate a blinking event."""
    record = {"blinkStrength": _rnd_percent()}
    return to_bytes(json.dumps(record))


def gen_familiarity():
    """Generate a familiarity event."""
    record = {"familiarity": _rnd_float()}
    return to_bytes(json.dumps(record))


def gen_mental_effort():
    """Generate a mental effort event."""
    record = {"mentalEffort": _rnd_float()}
    return to_bytes(json.dumps(record))
