"""Plot monitor data."""
__author__ = 'sb'

import matplotlib.pyplot as plt


def plot_raw_eeg_data(time_data, eeg_data):
    """Plot eeg_data as line plot.

    :param time_data: relative time info for data points in seconds.
    :type time_data: [float]
    :param eeg_data: values to plot.
    :type eeg_data: [float]
    """
    plt.plot(time_data, eeg_data, 'g-')
    plt.xlabel("time [secs]")
    plt.ylabel("raw EEG values")
    plt.title("EEG Data")
    plt.show()
