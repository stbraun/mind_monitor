#!/usr/bin/env python
import tkinter as tk
from tkinter import ttk
import log
import logging

from uicontrol import ControlPanel


class Application(ttk.Frame):
    """Mind Monitor Frontend"""

    def __init__(self, master=None):
        super().__init__(master, padding="3 3 12 12")
        self.logger = logging.getLogger('mind_monitor.ui')

        style = ttk.Style()
        style.configure('.', background='maroon', foreground='blue')

        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self):
        """Build UI."""
        ttk.Button(self, text='Quit', command=self.quit).grid(row=3, columnspan=2)

        create_control_panel = ControlPanel(self).panel
        create_control_panel.grid(row=2, columnspan=2, sticky=(tk.N, tk.W))

log.initialize_logger()
app = Application()
app.master.title('Mind Monitor')
app.mainloop()
