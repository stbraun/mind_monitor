# coding=utf-8
"""
Common definitions.
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


TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

# Indices into record tuple
idx_record = {'session': 0, 'timestamp': 1, 'highAlpha': 2, 'highBeta': 3, 'highGamma': 4,
              'delta': 5,
              'theta': 6,
              'lowAlpha': 7, 'lowBeta': 8, 'lowGamma': 9,
              'attention': 10, 'meditation': 11, 'poorSignalQuality': 12}

# Indices into raw data record
idx_raw = {'session': 0, 'timestamp': 1, 'data': 2}
