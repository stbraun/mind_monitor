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

from mindwavegenerator import MindWaveGenerator

HOST = ''
PORT = 13854
BUFFER_SIZE = 1024


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print('Connected by', addr)
    data = conn.recv(BUFFER_SIZE)
    print('Start serving ...')
    gen = MindWaveGenerator()
    for _ in range(5):
        rec = gen.gen_poor_signal()
        conn.sendall(rec+b'\n')
        print(rec)
        time.sleep(1)
    while True:
#    for _ in range(5):
        rec = gen.gen_power_record()
        conn.sendall(rec+b'\n')
        print(rec)
        time.sleep(1)
except BrokenPipeError:
    # client disconnected.
    pass
finally:
    print('shutting down ...')
    conn.close()
