from matplotlib.pylab import gca, figure, plot, subplot, title, xlabel, ylabel, xlim,show
import segment
import fit
from ebcli.lib.utils import urllib

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.lines import Line2D


def draw_plot(data, plt, plot_title):
    ax = plt.subplot2grid((3, 3), (0, 0), rowspan=1, colspan=4, axisbg='#07000d')
    ax.plot(range(len(data)), data, alpha=0.8, color='red')
    title(plot_title)
    xlabel("Samples")
    ylabel("Signal")
    xlim((0, len(data)-1))

def draw_segments(segments):
    ax = gca()
    for segment in segments:
        line = Line2D((segment[0],segment[2]),(segment[1],segment[3]))
        ax.add_line(line)

def bytespdate2num(fmt, encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)
    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)
    return bytesconverter

stockToFetch = input("Stock to plot: ")
max_error = float(input("Maximum error: "))
print(stockToFetch+" plot stock is preparing to be shown")
'''
    Use this to dynamically pull a stock:
'''
try:
    print('Currently Pulling',stockToFetch)
    urlToVisit = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+stockToFetch+'/chartdata;type=quote;range=10y/csv'
    stockFile =[]
    try:
        sourceCode = urllib.request.urlopen(urlToVisit).read().decode()
        splitSource = sourceCode.split('\n')
        for eachLine in splitSource:
            splitLine = eachLine.split(',')
            if len(splitLine) == 6:
                if 'values' not in eachLine:
                    stockFile.append(eachLine)
    except Exception as e:
        print(str(e), 'failed to organize pulled data.')
except Exception as e:
    print(str(e), 'failed to pull pricing data')

try:
    date, closep, highp, lowp, openp, volume = np.loadtxt(stockFile,delimiter=',', unpack=True,
                                                          converters={0: bytespdate2num('%Y%m%d')})
    x = 0
    y = len(date)
    newAr = []
    while x < y:
        appendLine = date[x], openp[x], highp[x], lowp[x], closep[x], volume[x]
        newAr.append(appendLine)
        x += 1

    my_dpi=96
    #sliding window with regression
    fig = plt.figure(num=None, figsize=(1280/my_dpi, 800/my_dpi), dpi=80, facecolor='w', edgecolor='k')
    segments = segment.slidingwindowsegment(closep, fit.regression, fit.sumsquared_error, max_error)
    draw_plot(closep,plt,"Sliding window with regression")
    draw_segments(segments)

    #bottom-up with regression
    segments = segment.bottomupsegment(closep, fit.regression, fit.sumsquared_error, max_error)
    draw_plot(closep,plt,"Bottom-up with regression")
    draw_segments(segments)

    #top-down with regression
    #figure()
    segments = segment.topdownsegment(closep, fit.regression, fit.sumsquared_error, max_error)
    draw_plot(closep,plt,"Top-down with regression")
    draw_segments(segments)



    #sliding window with simple interpolation
    #figure()
    segments = segment.slidingwindowsegment(closep, fit.interpolate, fit.sumsquared_error, max_error)
    draw_plot(closep,plt,"Sliding window with simple interpolation")
    draw_segments(segments)

    #bottom-up with  simple interpolation
    #figure()
    segments = segment.bottomupsegment(closep, fit.interpolate, fit.sumsquared_error, max_error)
    draw_plot(closep,plt,"Bottom-up with simple interpolation")
    draw_segments(segments)

    #top-down with  simple interpolation
    #figure()
    segments = segment.topdownsegment(closep, fit.interpolate, fit.sumsquared_error, max_error)
    draw_plot(closep,plt,"Top-down with simple interpolation")
    draw_segments(segments)


    show()

finally:
    print("OK DONE")


