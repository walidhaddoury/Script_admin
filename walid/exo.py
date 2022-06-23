import psutil
import logging
import sys
import time


def get_all_metrics(interval):
    while True:
        # CPU
        logging.info("%s", psutil.cpu_times())
        logging.info("%s", psutil.cpu_percent(interval=None, percpu=False))
        logging.info("%s", psutil.cpu_times_percent(interval=None, percpu=False))
        logging.info("%s", psutil.cpu_count(logical=True))
        logging.info("%s", psutil.cpu_stats())
        logging.info("%s", psutil.cpu_freq(percpu=False))
        logging.info("%s", psutil.getloadavg())

        # MEMORY
        logging.info("%s", psutil.virtual_memory())
        logging.info("%s", psutil.swap_memory())
        logging.info("%s", psutil.disk_partitions(all=False))
        logging.info("%s", psutil.disk_usage('/'))
        logging.info("%s", psutil.disk_io_counters(perdisk=False, nowrap=True))

        #NETWORK
        logging.info("%s", psutil.net_io_counters(pernic=False, nowrap=True))
        logging.info("%s", psutil.net_if_addrs())
        logging.info("%s", psutil.net_if_stats())

        # SENSORS
        logging.info("%s", psutil.sensors_battery())

        # OTHER SYS INFO
        logging.info("%s", psutil.boot_time())
        logging.info("%s", psutil.users())

        # PROCESSES
        logging.info("%s", psutil.pids())
        logging.info("%s", psutil.process_iter(attrs=None, ad_value=None))

        # OS
        logging.info("%s", psutil.MACOS)
        logging.info("%s", psutil.OSX)

        time.sleep(interval)


def main():
    if len(sys.argv) == 2:
        interval = int(sys.argv[1])
        get_all_metrics(interval)
    else:
        logging.error("Usage: %s", sys.argv[0])
        sys.exit(1)


if __name__ == '__main__':
    logging.basicConfig(filename="walid/metrics.log", level=logging.INFO,
                        format='%(asctime)s [ %(filename)s - l%(lineno)d : %(funcName)s ] - %(message)s')
    main()
