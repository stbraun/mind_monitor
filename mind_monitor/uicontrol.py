# coding=utf-8
"""
Control panel.
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


import tkinter as tk
from tkinter import ttk
import logging
from pkgutil import get_data

from .capture import CaptureEEGData


STATUS_SET = {'Idle': ('Idle', get_data('mind_monitor', '/resources/status_idle.gif')),
              'Running': ('Running ...', 'mind_monitor/resources/status_ok.gif'),
              'Stopped': ('Stopped', 'mind_monitor/resources/status_blue.gif'),
              'Warning': ('Warning', 'mind_monitor/resources/status_warning.gif'),
              'Error': ('Error', 'mind_monitor/resources/status_error.gif'),
              }

# Set TEST=True to work on the UI without accessing the device.
TEST = False


class ControlPanel(ttk.Frame):
    """Control panel for data gathering."""
    def __init__(self, master):
        self.logger = logging.getLogger('mind_monitor.ui')
        super().__init__(master, borderwidth=2, relief=tk.GROOVE)
        self.start_button = None
        self.stop_button = None
        self.raw_status = tk.IntVar()
        self.task = None
        self.__create_control_panel()

    def __create_control_panel(self):
        """Control panel for gathering EEG data."""
        ttk.Checkbutton(self, text='capture raw',
                        variable=self.raw_status).grid(row=1, column=0)

        self.start_button = ttk.Button(self, text='Start', command=self.start_action)
        self.start_button.grid(row=2, column=0)
        self.stop_button = ttk.Button(self, text='Stop', command=self.stop_action)
        self.stop_button.grid(row=2, column=1)
        self.stop_button.config(state='disabled')

        self.status = StatusPanel(self, STATUS_SET)
        self.status.grid(row=5, columnspan=2, sticky=(tk.W, tk.E))
        self.status.set_status('Idle')

    def start_action(self):
        """Callback start button."""
        self.logger.info('start_action')
        self.start_button.state(['disabled'])
        self.stop_button.state(['!disabled'])
        self.status.set_status('Running')
        if not TEST:
            self.task = CaptureEEGData(record_raw=(self.raw_status.get() == 1))
            self.task.start()

    def stop_action(self):
        """Callback stop button."""
        self.logger.info('stop_action')
        self.status.set_status('Stopped')
        if not TEST:
            self.task.stop()
            self.task.join(timeout=5)
        self.stop_button.state(['disabled'])
        self.start_button.state(['!disabled'])


class StatusPanel(ttk.Frame):
    """Present a status."""
    def __init__(self, master, status_set):
        super().__init__(master)
        self.logger = logging.getLogger('mind_monitor.ui')
        self.text = tk.StringVar()
        self.image = None
        self.status_set = status_set

    def set_status(self, status):
        """Set status to display.

        :param status: one of the status_set
        :raise Exception: in case of unknown status
        """
        if status not in self.status_set.keys():
            raise Exception('Invalid status: {}'.format(status))
        txt, img = self.status_set[status]
        self.logger.info('{} --> ({}, {})'.format(status, txt, img))
        photo = tk.PhotoImage(data=img)
        image = ttk.Label(self, image=photo)
        image.photo = photo
        image.grid(row=0, column=0, sticky=(tk.W))
        lbl = ttk.Label(self, textvariable=self.text)
        lbl.grid(row=0, column=1)
        self.text.set(txt)
