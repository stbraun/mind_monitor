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
from capture import CaptureEEGData


class ControlPanel(object):
    """Control panel for data gathering."""
    def __init__(self, master):
        self.logger = logging.getLogger('mind_monitor.ui')
        self.start_button = None
        self.stop_button = None
        self.raw_status = tk.IntVar()
        self.status = tk.StringVar()
        self.panel = self.__create_control_panel(master)
        self.task = None

    def __create_control_panel(self, master):
        """Control panel for gathering EEG data."""
        control_panel = ttk.Frame(master=master, borderwidth=2, relief=tk.GROOVE)
        ttk.Checkbutton(control_panel, text='capture raw', variable=self.raw_status).grid(row=1, column=0)

        self.start_button = ttk.Button(control_panel, text='Start', command=self.start_action)
        self.start_button.grid(row=2, column=0)
        self.stop_button = ttk.Button(control_panel, text='Stop', command=self.stop_action)
        self.stop_button.grid(row=2, column=1)
        self.stop_button.config(state='normal')

        self.status.set('Idle')
        ttk.Label(control_panel, textvariable=self.status).grid(row=5)
        control_panel.configure()
        return control_panel

    def start_action(self):
        """Callback start button."""
        self.logger.info('start_action')
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.status.set('Running...')
        self.task = CaptureEEGData(record_raw=(self.raw_status == 1))
        self.task.start()

    def stop_action(self):
        """Callback stop button."""
        self.logger.info('stop_action')
        self.status.set('Stopped')
        self.task.stop()
        self.task.join(timeout=5)
        self.stop_button.config(state='disabled')
        self.start_button.config(state='normal')
