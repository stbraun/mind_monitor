"""Plot monitor data."""
__author__ = 'sb'

import matplotlib.pyplot as plt


def plot_data(time_data, eeg_data, xlabel='Time [secs]', ylabel='Values', title='EEG Data'):
    """Plot eeg_data as line plot.

    :param xlabel: label for x axis.
    :param ylabel: label for y axis.
    :param title: title of the figure.
    :param time_data: relative time info for data points in seconds (time.time()).
    :type time_data: [float]
    :param eeg_data: values to plot.
    :type eeg_data: [float]
    """
    fig = plt.figure(num='EEG Plot', figsize=(18, 6))
    spl = fig.add_subplot(111, xlabel=xlabel, ylabel=ylabel, title=title)
    spl.plot(time_data, eeg_data, 'g-')
    return fig


def plot_raw_eeg_data(time_data, eeg_data):
    """Plot raw eeg data.

    :param time_data: relative time info for data points in seconds (time.time()).
    :type time_data: [float]
    :param eeg_data: values to plot.
    :type eeg_data: [float]
    """
    plot_data(time_data, eeg_data, ylabel='Raw values')
    plt.show()


def plot_theta_eeg_data(time_data, eeg_data):
    """Plot raw eeg data.

    :param time_data: relative time info for data points in seconds (time.time()).
    :type time_data: [float]
    :param eeg_data: values to plot.
    :type eeg_data: [float]
    """
    plot_data(time_data, eeg_data, ylabel='Theta')
    plt.show()


if __name__ == '__main__':
    x = [1, 2, 3, 4, 5]
    y = [0, 2, 4, 6, 8]
    plot_raw_eeg_data(x, y)
    plot_theta_eeg_data(x, y)
