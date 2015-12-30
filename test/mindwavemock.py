# coding=utf-8
"""
Mocks a MindWave device on socket level for testing.
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

import socket
import time

from mindwavegenerator import gen_poor_signal, gen_raw_record, gen_power_record

HOST = ''
PORT = 13854
BUFFER_SIZE = 1024


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = None
try:
    s.bind((HOST, PORT))
    print('Waiting for client to connect ...')
    s.listen(1)
    conn, address = s.accept()
    print('Connected by', address)
    data = conn.recv(BUFFER_SIZE)
    print('Start serving ...')
    for _ in range(5):
        rec = gen_poor_signal()
        conn.sendall(rec+b'\r')
        print(rec)
        time.sleep(0.5)
    while True:
        for _ in range(10):
            rec = gen_raw_record()
            conn.sendall(rec + b'\r')
            print(rec)
            time.sleep(0.1)
        rec = gen_power_record()
        conn.sendall(rec+b'\r')
        print(rec)
except BrokenPipeError:
    # client disconnected.
    pass
finally:
    print('shutting down ...')
    if conn is not None:
        conn.close()
