#!/usr/bin/python

import sys
import getopt

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from pylab import rcParams

from config import *
from reload_battery_logs import reload_logs

rcParams['figure.figsize'] = 10, 5


class COLOR:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class MOTE_FLOW_STATES:
    REGULAR_SLEEP = 'regular sleep'
    DEVICE_IDLE = 'Device idle for 30s'
    READY_TO_SLEEP = 'ready to sleep'
    CONNECTING_TO_WIFI = 'connecting_to_wifi'
    CONNECTED_TO_WIFI = 'connected_to_wifi'
    STARTING_LSM = 'starting lsm6ds3'


class ANALYSIS_TASKS:
    MEASUREMENT_CYCLE_TIME = 'measurement_cycle_time'
    SLEEP_REASON = 'sleep_reason'
    WIFI_RSSI_TREND = 'wifi_rssi_trend'
    BATTERY_TREND = 'battery_voltage_trend'
    RELOAD_LOGS = 'reload_logs'

    @classmethod
    def all(cls):
        return [
            cls.MEASUREMENT_CYCLE_TIME,
            cls.SLEEP_REASON,
            cls.WIFI_RSSI_TREND,
            cls.BATTERY_TREND,
            cls.RELOAD_LOGS
        ]


def run_sleep_reason_analysis():
    result = []
    for device_id in context.device_id_list:
        data = pd.read_csv('data/' + device_id + '.csv')
        data['TIMESTAMP'] = pd.to_datetime(
            data['TIMESTAMP'],
            format='%Y-%m-%d %H:%M:%S'
        )
        regular_sleep_data = data[data['REASON'] == MOTE_FLOW_STATES.REGULAR_SLEEP]
        device_idle_sleep_data = data[data['REASON'] == MOTE_FLOW_STATES.DEVICE_IDLE]
        result.append([
            device_id,
            len(regular_sleep_data.index),
            len(device_idle_sleep_data.index),
            len(regular_sleep_data[regular_sleep_data['TIMESTAMP'] > context.start_date].index),
            len(device_idle_sleep_data[device_idle_sleep_data['TIMESTAMP'] > context.start_date].index)
        ])

    result = np.array(result)
    result_df = pd.DataFrame(
        np.array(result),
        columns=[
            'Device Id',
            'Regular sleep total count',
            'Device idle sleep total count',
            'Regular sleep count since install',
            'Device idle sleep count since install'
        ]
    )
    result_df.to_csv(result_base_url + context.account + '_motes_sleep_reason_analysis.csv')


def measurement_cycle_time_analysis():
    result = []
    for device_id in context.device_id_list:
        data = pd.read_csv('data/' + device_id + '.csv')
        data['TIMESTAMP'] = pd.to_datetime(
            data['TIMESTAMP'],
            format='%Y-%m-%d %H:%M:%S'
        )
        data = data[data['TIMESTAMP'] > context.start_date]
        start_timestamps = data[data['REASON'] == MOTE_FLOW_STATES.STARTING_LSM]['TIMESTAMP'].tolist()
        f1 = data['REASON'] == MOTE_FLOW_STATES.READY_TO_SLEEP
        f2 = data['TIMESTAMP'] > start_timestamps[0]
        filtered_result = f1 & f2
        end_timestamps = data[filtered_result]['TIMESTAMP'].tolist()
        start_wifi_timestamps = data[data['REASON'] == MOTE_FLOW_STATES.CONNECTING_TO_WIFI]['TIMESTAMP'].tolist()
        f1 = data['REASON'] == MOTE_FLOW_STATES.CONNECTED_TO_WIFI
        f2 = data['TIMESTAMP'] > start_wifi_timestamps[0]
        filtered_result = f1 & f2
        end_wifi_timestamps = data[filtered_result]['TIMESTAMP'].tolist()
        diff = len(start_wifi_timestamps) - len(end_wifi_timestamps)
        if diff:
            l = len(start_wifi_timestamps)
            start_wifi_timestamps = start_wifi_timestamps[0:l-diff]

        measurement_cycle_times = []
        wifi_connect_times = []
        for i in range(len(start_timestamps)):
            cycle_time = (end_timestamps[i] - start_timestamps[i]).total_seconds()
            if cycle_time > 0:
                measurement_cycle_times.append(cycle_time)

        for i in range(len(end_wifi_timestamps)):
            wifi_connect_time = (end_wifi_timestamps[i] - start_wifi_timestamps[i]).total_seconds()
            if 0 < wifi_connect_time < 50:
                wifi_connect_times.append(wifi_connect_time)

        if len(measurement_cycle_times) == 0 or len(wifi_connect_times) == 0:
            continue

        result.append([
            device_id,
            len(measurement_cycle_times),
            measurement_cycle_times[-1],
            np.mean(measurement_cycle_times),
            wifi_connect_times[-1],
            np.mean(wifi_connect_times)
        ])

    result = np.array(result)
    result_df = pd.DataFrame(
        np.array(result),
        columns=[
            'Device Id',
            'Number of cycles',
            'Last measurement cycle time(in seconds)',
            'Average measurement cycle time(in seconds)',
            'Last wifi connect time(in seconds)',
            'Average wifi connect time(in seconds)'
        ]
    )
    result_df.to_csv(result_base_url + context.account + '_motes_measurement_cycle_time_analysis.csv')


def plot_rssi_histogram():
    result = []
    for device_id in context.device_id_list:
        data = pd.read_csv('data/' + device_id + '.csv')
        data['TIMESTAMP'] = pd.to_datetime(data['TIMESTAMP'], format='%Y-%m-%d %H:%M:%S')
        f1 = data['TIMESTAMP'] > context.start_date
        f2 = data['REASON'] == MOTE_FLOW_STATES.CONNECTED_TO_WIFI
        data = data[f1 & f2]
        rssi_list = data['WIFI_RSSI'].tolist()
        result.append([
            device_id,
            rssi_list[-1],
            data['WIFI_RSSI'].mean()
        ])
        plt.hist(rssi_list)
        plt.title("Wifi rssi Histogram for %s" % device_id)
        plt.xlabel("Value")
        plt.ylabel("Frequency")
        #plt.show()
        plt.savefig(chart_base_url + context.account + '_' + device_id + '_wifi_rssi_distribution.png')
        plt.clf()

    result = np.array(result)
    result_df = pd.DataFrame(
        np.array(result),
        columns=[
            'Device Id',
            'Last WIFI RSSI',
            'Average WIFI RSSI'
        ]
    )
    result_df.to_csv(result_base_url + context.account + '_motes_wifi_rssi_analysis.csv')


def plot_battery_voltage_trend():
    result = []
    for device_id in context.device_id_list:
        data = pd.read_csv('data/' + device_id + '.csv')
        data['TIMESTAMP'] = pd.to_datetime(data['TIMESTAMP'], format='%Y-%m-%d %H:%M:%S')
        f1 = data['TIMESTAMP'] > context.start_date
        f2 = data['REASON'] == MOTE_FLOW_STATES.STARTING_LSM
        data = data[f1 & f2]
        battery_voltage_list = data['BATTERY_VOLTAGE'].tolist()
        timestamps = data['TIMESTAMP'].tolist()
        result.append([
            device_id,
            battery_voltage_list[-1],
            data['BATTERY_VOLTAGE'].mean()
        ])
        save_chart(
            timestamps,
            battery_voltage_list,
            chart_base_url + context.account + '_' + device_id + '_battery_level_trend.png',
            title="Battery voltage trend for %s" % device_id,
            x_label="Time",
            y_label="Battery Voltage"
        )

    result = np.array(result)
    result_df = pd.DataFrame(
        np.array(result),
        columns=[
            'Device Id',
            'Last battery voltage',
            'Average battery voltage'
        ]
    )
    result_df.to_csv(result_base_url + context.account + '_motes_voltage_level_analysis.csv')


def save_chart(x_data, y_data, file_name, title="", x_label="", y_label=""):
    plt.close('all')
    fig, ax = plt.subplots(1)
    ax.plot(x_data, y_data)
    # rotate and align the tick labels so they look better
    fig.autofmt_xdate()
    # use a more precise date string for the x axis locations in the toolbar
    ax.fmt_xdata = mdates.DateFormatter('%d-%m-%y')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(file_name)
    plt.clf()


def print_usage():
    print COLOR.BOLD + "Usage:" + COLOR.END
    print COLOR.BLUE + 'python battery_log_analysis.py -d <device_group> -t <task>' + COLOR.END
    print COLOR.BOLD + "Allowed tasks:" + COLOR.END
    tasks = ANALYSIS_TASKS.all()
    for i in range(len(tasks)):
        print COLOR.YELLOW + "%s. %s" % (i, tasks[i]) + COLOR.END


def main(argv):
    device_group = None
    task = None
    try:
        opts, args = getopt.getopt(argv, "hd:t:", ["device_group=", "task="])
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit()
        elif opt in ("-d", "--device_group"):
            device_group = arg
        elif opt in ("-t", "--task"):
            task = arg

    if device_group is None or task is None:
        print "Invalid usage"
        print_usage()
        sys.exit(2)

    if device_group not in account_motes.keys():
        print device_group + " device group not configured"
        sys.exit(2)

    context.set_account(device_group)

    if task == ANALYSIS_TASKS.BATTERY_TREND:
        plot_battery_voltage_trend()
        print "Battery trend analysis successful. Results can be found in results/charts directory"
    elif task == ANALYSIS_TASKS.WIFI_RSSI_TREND:
        plot_rssi_histogram()
        print "WIFI rssi trend analysis successful. Results can be found in results/charts directory"
    elif task == ANALYSIS_TASKS.MEASUREMENT_CYCLE_TIME:
        measurement_cycle_time_analysis()
        print "Measurement cycle time analysis successful. Results can be found in results directory"
    elif task == ANALYSIS_TASKS.SLEEP_REASON:
        run_sleep_reason_analysis()
        print "Device sleep reason analysis successful. Results can be found in results directory"
    elif task == ANALYSIS_TASKS.RELOAD_LOGS:
        reload_logs()
    else:
        print "Invalid task name"
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])