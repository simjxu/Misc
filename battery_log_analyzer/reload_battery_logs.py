import time
import urllib

from config import *


def reload_logs():
    reload_start = time.time()
    for device_id in context.device_id_list:
        start = time.time()
        print("Downloading logs for mote: %s..." % device_id)
        file_name = device_id + '.csv'
        url = battery_logs_download_base_url + file_name
        try:
            urllib.urlretrieve(url, battery_logs_base_url + file_name)
        except IOError:
            print("Connection timed out")
            continue

        end = time.time()
        print("Download time: %s" % (end - start))

    print("Total download time: %s" % (time.time() - reload_start))

if __name__ == '__main__':
    reload_logs()