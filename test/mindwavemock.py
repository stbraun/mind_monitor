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

HOST = ''
PORT = 13854
BUFFER_SIZE = 1024
MAX_QUALITY_LEVEL = 200
POOR_SIGNAL_LEVEL = 'poorSignalLevel'

msg_bad_quality = b'{"poorSignalLevel": 200}\n'
msg_good_quality = b'{"eSense" : { "meditation" : 75, "attention" : 54 }, "poorSignalLevel" : 0, "eegPower" : { "delta" : 874006, "lowGamma" : 3197, "theta" : 53351, "lowBeta" : 6113, "highBeta" : 9367, "lowAlpha" : 36106, "highGamma" : 27478, "highAlpha" : 9544 } }\n'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    print('Connected by', addr)
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break
        for _ in range(10):
            conn.sendall(msg_bad_quality)
        for _ in range(20):
            conn.sendall(msg_good_quality)
finally:
    print('shutting down ...')
    conn.close()
