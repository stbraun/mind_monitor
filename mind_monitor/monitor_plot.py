"""Plot monitor data."""

import matplotlib.pyplot as plt

from monitor_common import idx_record


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


def plot_records(records, t_base=None):
    """Plot all power data.

    :param records: the data records as list of tuples.
    :param t_base: optional base value for time.
    """
    if len(records) > 0:
        session_id = records[0][idx_record['session']]
        if t_base is None:
            t_base = records[0][1]
        t_data = [x[idx_record['timestamp']] - t_base for x in records]
        delta_data = [x[idx_record['delta']] for x in records]
        theta_data = [x[idx_record['theta']] for x in records]
        fig = plt.figure(figsize=(15, 12))

        spl1 = fig.add_subplot(411,
                               xlabel='time [sec]',
                               ylabel='value',
                               title='EEG data for session {}'.format(session_id))
        spl1.plot(t_data, delta_data, label='delta')
        spl1.plot(t_data, theta_data, label='theta')
        spl1.legend(loc='best')

        high_alpha_data = [x[idx_record['highAlpha']] for x in records]
        high_beta_data = [x[idx_record['highBeta']] for x in records]
        high_gamma_data = [x[idx_record['highGamma']] for x in records]

        spl2 = fig.add_subplot(412,
                               xlabel='time [sec]',
                               ylabel='value')
        spl2.plot(t_data, high_alpha_data, label='highAlpha')
        spl2.plot(t_data, high_beta_data, label='highBeta')
        spl2.plot(t_data, high_gamma_data, label='highGamma')
        spl2.legend(loc='best')

        low_alpha_data = [x[idx_record['lowAlpha']] for x in records]
        low_beta_data = [x[idx_record['lowBeta']] for x in records]
        low_gamma_data = [x[idx_record['lowGamma']] for x in records]

        spl3 = fig.add_subplot(413,
                               xlabel='time [sec]',
                               ylabel='value')
        spl3.plot(t_data, low_alpha_data, label='lowAlpha')
        spl3.plot(t_data, low_beta_data, label='lowBeta')
        spl3.plot(t_data, low_gamma_data, label='lowGamma')
        spl3.legend(loc='best')

        attention_data = [x[idx_record['attention']] for x in records]
        meditation_data = [x[idx_record['meditation']] for x in records]

        spl4 = fig.add_subplot(414,
                               xlabel='time [sec]',
                               ylabel='%')
        spl4.plot(t_data, attention_data, label='attention')
        spl4.plot(t_data, meditation_data, label='meditation')
        spl4.legend(loc='best')

        plt.show()


if __name__ == '__main__':
    x = [1, 2, 3, 4, 5]
    y = [0, 2, 4, 6, 8]
    plot_raw_eeg_data(x, y)
    plot_theta_eeg_data(x, y)
