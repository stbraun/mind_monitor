#!/usr/bin/env python
"""
MindMonitor main module.
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

import tkinter as tk
from tkinter import ttk
import logging

from .log import initialize_logger
from .uicontrol import ControlPanel
from .uigraph import PowerGraphs, FeedGraphData


class Application(ttk.Frame):
    """Mind Monitor Frontend"""

    def __init__(self, master=None):
        super().__init__(master, padding="3 3 12 12")
        self.logger = logging.getLogger('mind_monitor.ui')

        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self):
        """Build UI."""
        control_panel = ControlPanel(self)
        control_panel.grid(row=0, column=0, sticky=tk.N)
        graph_panel = PowerGraphs(self)
        feed_panel = FeedGraphData(self, graph_panel)
        feed_panel.grid(row=1, column=0, sticky=tk.N)
        graph_panel.grid(row=0, column=1, rowspan=3, sticky=(tk.N, tk.W))

        # TASK handle quit in a more sensible way, e.g. wait for threads to
        # terminate ...
        ttk.Button(self, text='Quit', command=self.quit).grid(row=2, column=0,
                                                              sticky=tk.S)


if __name__ == '__main__':
    initialize_logger()
    APP = Application()
    APP.master.title('Mind Monitor')
    APP.mainloop()
