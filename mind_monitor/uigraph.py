# coding=utf-8
"""
PowerGraphs.
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

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas
from .monitor_sqlite import SQLiteDB


class PowerGraphs(ttk.Frame):
    """Graphical representation of EEG data."""

    def __init__(self, master):
        self.logger = logging.getLogger('mind_monitor.ui')
        super().__init__(master, borderwidth=2, relief=tk.GROOVE)
        self.fig = Figure(figsize=(15, 12))
        self.subplot_base = 410
        self.canvas = FigureCanvas(self.fig, master=self)
        self.canvas.get_tk_widget().grid()
        self.fig.clear()

    def plot_records(self, records, raw_records=None, t_base=None):
        """Plot all power data.

        :param records: the data records as list of tuples.
        :param raw_records: optional raw records.
        :param t_base: optional base value for time.
        """
        self.logger.info('Ready to plot {} records ...'.format(len(records)))
        self.fig.clear()
        if len(records) > 0:
            if raw_records:
                session_id = raw_records[0].session
                if t_base is None:
                    t_base = raw_records[0].timestamp
                t_raws = [x.timestamp - t_base for x in raw_records]
                self.subplot_base = 511
                # raw wave
                raw_data = [x.data for x in raw_records]
                spl0 = self.fig.add_subplot(self._subplot_id(0),
                                            xlabel='time [sec]',
                                            ylabel='value',
                                            title='EEG raw data for session '
                                                  '{}'.format(
                                                session_id))
                spl0.plot(t_raws, raw_data, label='raw')
            session_id = records[0].session
            if t_base is None:
                t_base = records[0].timestamp
            t_data = [x.timestamp - t_base for x in records]
            # delta and theta waves
            delta_data = [x.delta for x in records]
            theta_data = [x.theta for x in records]
            spl1 = self.fig.add_subplot(self._subplot_id(1),
                                        xlabel='time [sec]',
                                        ylabel='value',
                                        title='EEG power data for session {'
                                              '}'.format(
                                            session_id))
            # self.canvas.ylim((0, 500000))
            spl1.semilogy(t_data, delta_data, label='delta')
            spl1.semilogy(t_data, theta_data, label='theta')
            spl1.legend(loc='best')

            # high alpha, beta, gamma waves
            high_alpha_data = [x.highAlpha for x in records]
            high_beta_data = [x.highBeta for x in records]
            high_gamma_data = [x.highGamma for x in records]

            spl2 = self.fig.add_subplot(self._subplot_id(2),
                                        xlabel='time [sec]',
                                        ylabel='value')
            # self.canvas.ylim((0, 70000))
            spl2.semilogy(t_data, high_alpha_data, label='highAlpha')
            spl2.semilogy(t_data, high_beta_data, label='highBeta')
            spl2.semilogy(t_data, high_gamma_data, label='highGamma')
            spl2.legend(loc='best')

            # low alpha, beta, gamma waves
            low_alpha_data = [x.lowAlpha for x in records]
            low_beta_data = [x.lowBeta for x in records]
            low_gamma_data = [x.lowGamma for x in records]

            spl3 = self.fig.add_subplot(self._subplot_id(3),
                                        xlabel='time [sec]',
                                        ylabel='value')
            # self.canvas.ylim((0, 70000))
            spl3.semilogy(t_data, low_alpha_data, label='lowAlpha')
            spl3.semilogy(t_data, low_beta_data, label='lowBeta')
            spl3.semilogy(t_data, low_gamma_data, label='lowGamma')
            spl3.legend(loc='best')

            # attention and meditaion waves
            attention_data = [x.attention for x in records]
            meditation_data = [x.meditation for x in records]

            spl4 = self.fig.add_subplot(self._subplot_id(4),
                                        xlabel='time [sec]',
                                        ylabel='%')
            spl4.plot(t_data, attention_data, label='attention')
            spl4.plot(t_data, meditation_data, label='meditation')
            spl4.legend(loc='best')

            self.canvas.show()

    def _subplot_id(self, cnt):
        """Generate subplot id.

        :param cnt: number of subplot.
        :type cnt: int
        :return: generated id
        :rtype: int
        """
        return self.subplot_base + cnt


class FeedGraphData(ttk.Frame):
    """Provide data for PowerGraphs."""

    def __init__(self, master, graph_panel):
        self.logger = logging.getLogger('mind_monitor.ui')
        super().__init__(master, borderwidth=2, relief=tk.GROOVE)
        self.graph_panel = graph_panel
        self.database = None
        self.session_entry = None
        self.plot_btn = None
        self.lbl_session_id = tk.StringVar()
        self.lbl_session_id.set('Enter session id for plotting:')
        self.setup_ui()

    def setup_ui(self):
        """Create widgets."""
        ttk.Label(self, textvariable=self.lbl_session_id).grid(row=0, column=0)
        self.session_entry = ttk.Entry(self)
        self.session_entry.grid(row=1, column=0)
        self.plot_btn = ttk.Button(self, text='plot data',
                                   command=self.__retrieve_data)
        self.plot_btn.grid(row=2, column=0)

    def __connect_db(self):
        '''Connect to database.'''
        self.database = SQLiteDB()

    def __close_connection(self):
        '''Close database connection.'''
        if self.database is not None:
            self.database.close()

    def __retrieve_data(self):
        '''Retrieve data from database and feed into graph panel.'''
        self.__connect_db()
        session_id = self.session_entry.get()
        self.logger.info(
            'retrieving data for session {} ...'.format(session_id))
        records = self.database.retrieve_data(session_id)
        raw_records = self.database.retrieve_raw_data(session_id)
        self.__close_connection()
        self.logger.info('{} records retrieved'.format(len(records)))
        self.graph_panel.plot_records(records, raw_records=raw_records)
