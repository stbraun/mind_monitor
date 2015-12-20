#!/usr/bin/env python
import tkinter as tk
from tkinter import ttk
import log
import logging

from uicontrol import ControlPanel
from uigraph import PowerGraphs, FeedGraphData


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

        # TASK handle quit in a more sensible way, e.g. wait for threads to terminate ...
        ttk.Button(self, text='Quit', command=self.quit).grid(row=2, column=0, sticky=tk.S)

log.initialize_logger()
app = Application()
app.master.title('Mind Monitor')
app.mainloop()
