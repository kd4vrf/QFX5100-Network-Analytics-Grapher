#!/usr/bin/env python
# -*- coding: utf-8 -*-
import getopt
import sys
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import matplotlib.ticker as ticker
from pylab import rcParams

data = []
interface_list = []

def convert_datetime(timestamp):
    epoch = datetime.datetime(1970, 1, 1)
    converted_datetime = epoch + datetime.timedelta(microseconds=timestamp)
    return converted_datetime

try:
    opts, args = getopt.getopt(sys.argv[1:],"hf:b:",["file="])
except getopt.GetoptError:
    print '\n' * 2
    print 'usage: python raptor.py -f <filename>'
    print 'where <filename> is the name of the buffer output file'
    print 'where <min_buffer_threshold> is the minumum size buffer event you want to see'
    print 'example: python raptor.py -f an -b 208'
    print '\n' * 2
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print '\n' * 2
        print 'usage: python raptor.py -f <filename> -i <interface> -b <min_buffer_threshold>'
        print 'where <filename> is the name of the buffer output file'
        print 'where <min_buffer_threshold> is the minumum size buffer event you want to see'
        print 'example: python raptor.py -f an -b 208'
        print '\n' * 2
        sys.exit()
    elif opt in ('-f', '--file'):
        filename = arg
        file = open(filename, "r")
    elif opt in ('-b', '--buffer_size'):
        buffer_size = arg
    else:
        pass

def collect_data():
    for line in file:
        line = line.strip()
        value = line.split(',')
        data.append(value)
        if value[0] == "q":
            interface_list.append(value[3])


def plot_engine(func_interface):
    x_axis = []
    y_axis = []
    for item in data:
        if item[0] == "q":
            if item[3] == func_interface:
                if int(item[5]) >= int(buffer_size):
                    print "{3} \t {0} \t latency(nanoseconds): {1} \t buffer(bytes): {2}".format(
                        convert_datetime(int(item[1])),
                        item[4],
                        item[5],
                        item[3]
                        )
                    x_value = convert_datetime(int(item[1]))
                    x_axis.append(x_value)
                    y_axis.append(int(item[5]))


    rcParams['figure.figsize'] = 15, 6
    fig, ax = plt.subplots()
    ax.plot(x_axis, y_axis)
    ax.set_title(func_interface)
    ax.set_yticks([26000, 50000, 100000, 150000, 200000, 250000, 300000, 400000])
    ax.get_yticklabels()[0].set_color("red")
    plt.axhline(26000, color='red', linestyle='-')
    plt.ylim( [0,400000]) #Scale of y_axis 4992000
    plt.ylabel('Buffer Size in Bytes')
    plt.xlabel('Time Stamp UTC')
    ax.set_xticks(ax.get_xticks()[::1])
    plt.grid(True)
    fig.autofmt_xdate()

def plot_all_unique():
    unique_interface_list = list(set(interface_list))
    print len(unique_interface_list)
    for item in unique_interface_list:
        plot_engine(item)

collect_data()
plot_all_unique()
plt.show()

file.close()
