import getopt
import sys
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import matplotlib.ticker as ticker
from pylab import rcParams


def convert_datetime(timestamp):
    epoch = datetime.datetime(1970, 1, 1)
    converted_datetime = epoch + datetime.timedelta(microseconds=timestamp)
    return converted_datetime

try:
    opts, args = getopt.getopt(sys.argv[1:],"hf:i:b:",["file="])
except getopt.GetoptError:
    print '\n' * 2
    print 'usage: python raptor.py -f <filename>'
    print 'where <filename> is the name of the buffer output file'
    print 'where <interface> is the interface to show statistics for'
    print 'where <min_buffer_threshold> is the minumum size buffer event you want to see'
    print 'example: python raptor.py -f an -i xe-0/0/14 -b 208'
    print '\n' * 2
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print '\n' * 2
        print 'usage: python raptor.py -f <filename> -i <interface> -b <min_buffer_threshold>'
        print 'where <filename> is the name of the buffer output file'
        print 'where <interface> is the interface to show statistics for'
        print 'where <min_buffer_threshold> is the minumum size buffer event you want to see'
        print 'example: python raptor.py -f an -i xe-0/0/14 -b 208'
        print '\n' * 2
        sys.exit()
    elif opt in ('-f', '--file'):
        filename = arg
        file = open(filename, "r")
    elif opt in ('-i', '--interface'):
        interface = arg
    elif opt in ('-b', '--buffer_size'):
        buffer_size = arg
    else:
        pass

def plot_engine(func_interface):
    x_axis = []
    y_axis = []
    for line in file:
        line = line.strip()
        value = line.split(',')
        if value[0] == "q":
            if value[3] == func_interface:
                if int(value[5]) >= int(buffer_size):
                    print "{3} \t {0} \t latency: {1} \t buffer: {2}".format(
                        convert_datetime(int(value[1])),
                        value[4],
                        value[5],
                        value[3]
                        )
                    x_value = convert_datetime(int(value[1]))
                    x_axis.append(x_value)
                    y_axis.append(int(value[5]))

    rcParams['figure.figsize'] = 15, 6
    fig, ax = plt.subplots()
    ax.plot(x_axis, y_axis)
    ax.set_title(func_interface)
    plt.ylim( [0,350000]) #Scale of y_axis 4992000
    plt.ylabel('Buffer Size in Bytes')
    plt.xlabel('Time Stamp UTC')
    ax.set_xticks(ax.get_xticks()[::1])
    plt.grid(True)
    fig.autofmt_xdate()


plot_engine(interface)
plt.show()


file.close()
