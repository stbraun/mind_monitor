# coding=utf-8
"""
A publisher for arbitrary messages.
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

from contextlib import contextmanager
import time
import zmq


@contextmanager
def publish(port, protocol='tcp',):
        context = zmq.Context()
        publisher = context.socket(zmq.PUB)
        url = '{}://*:{}'.format(protocol, port)
        publisher.bind(url)
        # Short sleep seems to be required before first call to publisher.send_multipart().
        # TASK check
        time.sleep(0.1)
        yield publisher

        publisher.close()
        context.term()


def __test():
    with publish('12345') as pub:
        for i in range(5):
            print('sending message using {}'.format(pub))
            pub.send_multipart([b"sh", bytes("I'm publishing {}".format(i), encoding="utf-8")])
            print('message sent.')
    print('closed')
