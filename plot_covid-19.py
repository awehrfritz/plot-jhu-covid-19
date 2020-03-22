#!/usr/bin/env python

"""
Plot COVID-19 numbers
"""

import os
import sys
import time
import urllib
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'


def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count*block_size)
    speed = int(progress_size/(1024*duration))
    percent = int(count*block_size*100/total_size)
    unit, f = 'KB', 1024
    if progress_size > 1024*1024:
        unit, f = 'MB', 1024*1024
    if progress_size > 1024*1024*1024:
        unit, f = 'GB', 1024*1024*1024
    sys.stdout.write("\r...%d%%, %d %s, %d KB/s, %d seconds passed" %
                    (percent, progress_size/f, unit, speed, duration))
    sys.stdout.flush()


if __name__ == "__main__":
    # Parse command-line arguments
    import argparse
    parser = argparse.ArgumentParser(usage=__doc__)
    parser.add_argument("-e", "--fig-ext", type=str, default=None)
    parser.add_argument("-d", "--download", default=False, action="store_true")
    parser.add_argument("-c", "--countries", type=str, nargs='+')
    parser.add_argument("-s", "--plot-states", default=False, action="store_true")
    parser.add_argument("-t", "--plot-total", default=False, action="store_true")
    args = parser.parse_args()

    fname = os.path.basename(URL)
    if args.download or (not os.path.isfile(fname)):
        try:
            urllib.request.urlretrieve(URL, fname, reporthook)
        except urllib.error.HTTPError as ex:
            print('Problem:', ex)
    df = pd.read_csv(fname)
    idx = df.keys()[4]
    time = pd.to_datetime(df.keys()[4:])

    if not args.countries:
        args.plot_total = True

    plt.close('all')
    fig, ax = plt.subplots()
    if args.plot_total:
        # Total cases
        cases = df.loc[:,idx:].sum()
        ax.plot(time, cases, '.-', label='Total')
    for c in args.countries:
        # Cases per country
        data = df[df['Country/Region'] == c]
        cases = data.loc[:,idx:].sum()
        ax.plot(time, cases, '.-', label=c)
        if args.plot_states and (len(data) > 1):
            # Cases per state
            states = data['Province/State']
            for s in states:
                cases = data[data['Province/State'] == s].loc[:,idx:].sum()
                ax.plot(time, cases, '.--', label=c + ' - ' + s)
    ax.legend(loc='best')
    ax.set_title('COVID-19')
    ax.set_ylabel('Confirmed cases')
    #ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.fmt_xdata = mdates.DateFormatter('%d %b')
    ax.xaxis.set_major_formatter(ax.fmt_xdata)

    fig.autofmt_xdate()
    fig_name = 'covid-19-%s' % ('_'.join(args.countries))
    if args.fig_ext:
        fname_fig = os.path.join('./', '%s.%s' % (fig_name, args.fig_ext))
        print('Save figure to: %s' % (fname_fig))
        fig.savefig(fname_fig, dpi=200)
    fig.tight_layout()
    fig.show()
    fig.canvas.set_window_title(fig_name)
    fig.canvas.manager.window.activateWindow()
    fig.canvas.manager.window.raise_()
