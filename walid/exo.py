import psutil
import logging
import sys
import time

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate an API token from the "API Tokens Tab" in the UI
token = "liGC8MH4qtl9B3X6yrZw473XIDLjx6uxsR008bktiGh8W4bMl4JJ7pnEggLnEOSzGKnhaU6caKlamiHfIYZdiQ=="
org = "alexis.majchrzak77@gmail.com"
bucket = "python_bdd"


def get_cpu_metrics():
    """Get list of cpu metrics.

        sends in metrics logs
    """
    logging.info("%s", psutil.cpu_times()[0])
    post_cpu_metrics("cpu_time", str(psutil.cpu_times()[0]))

    logging.info("%s", psutil.cpu_percent(interval=0.1, percpu=False))
    post_cpu_metrics("cpu_percent", str(psutil.cpu_percent(interval=0.1, percpu=False)))

    logging.info("%s", psutil.cpu_times_percent(interval=0.1, percpu=False)[0])
    post_cpu_metrics("cpu_times_percent", str(psutil.cpu_times_percent(interval=0.1, percpu=False)[0]))

    logging.info("%s", psutil.cpu_count(logical=True))
    post_cpu_metrics("cpu_count", str(psutil.cpu_count(logical=True)))

    logging.info("%s", psutil.cpu_stats()[0])
    post_cpu_metrics("cpu_stats", str(psutil.cpu_stats()[0]))

    logging.info("%s", psutil.cpu_freq(percpu=False)[0])
    post_cpu_metrics("cpu_freq", str(psutil.cpu_freq(percpu=False)[0]))

    logging.info("%s", psutil.getloadavg()[0])
    post_cpu_metrics("cpu_getLoadvg", str(psutil.getloadavg()[0]))


def post_cpu_metrics(field, data):
    """Send metrics in database.

        Parameters
        ----------
        field : string
        data: string
    """
    table = "CPU,"
    print(data)

    with InfluxDBClient(url="https://us-east-1-1.aws.cloud2.influxdata.com", token=token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        request = table + "host=host1 " + field + "=" + data  # changer ici pour rentrer les metrics
        write_api.write(bucket, org, request)


def get_memory_metrics():
    """Get list of memory metrics.

        sends in metrics logs
    """
    logging.info("%s", psutil.virtual_memory()[0])
    post_memory_metrics("memory_virtual_memory", str(psutil.virtual_memory()[0]))

    logging.info("%s", psutil.swap_memory()[0])
    post_memory_metrics("memory_swap_memory", str(psutil.swap_memory()[0]))

    # logging.info("%s", psutil.disk_partitions(all=False)[0].device)
    # post_memory_metrics("memory_disk_partitions", str(psutil.disk_partitions(all=False)[0].device))

    logging.info("%s", psutil.disk_usage('/')[0])
    post_memory_metrics("memory_disk_usage", str(psutil.disk_usage('/')[0]))

    logging.info("%s", psutil.disk_io_counters(perdisk=False, nowrap=True)[0])
    post_memory_metrics("memory_disk_io_counters", str(psutil.disk_io_counters(perdisk=False, nowrap=True)[0]))


def post_memory_metrics(field, data):
    """Converting the input to a list.

        Parameters
        ----------
        field : string
        data: string
    """

    table = "MEMORY,"
    print(data)

    with InfluxDBClient(url="https://us-east-1-1.aws.cloud2.influxdata.com", token=token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        request = table + "host=host1 " + field + "=" + data  # changer ici pour rentrer les metrics
        write_api.write(bucket, org, request)


def get_network_metrics():
    """Get list of network metrics.

        sends in metrics logs
    """
    logging.info("%s", psutil.net_io_counters(pernic=False, nowrap=True))
    logging.info("%s", psutil.net_if_addrs())
    logging.info("%s", psutil.net_if_stats())


def get_sensor_metrics():
    """Get list of sensor metrics.

        sends in metrics logs
    """
    logging.info("%s", psutil.sensors_battery())


def get_other_info_sys_metrics():
    """Get list of other info sys metrics.

        sends in metrics logs
    """
    logging.info("%s", psutil.boot_time())
    logging.info("%s", psutil.users())


def get_process_metrics():
    """Get list of process metrics.

        sends in metrics logs
    """
    logging.info("%s", psutil.pids())
    logging.info("%s", psutil.process_iter(attrs=None, ad_value=None))


def get_os_metrics():
    """Get list of os metrics.

        sends in metrics logs
    """
    logging.info("%s", psutil.MACOS)
    logging.info("%s", psutil.OSX)


def get_all_metrics(interval):
    """Get list of all metrics.

        sends in metrics logs
    """
    while True:
        get_cpu_metrics()
        get_memory_metrics()

        # get_os_metrics()
        # get_process_metrics()
        # get_network_metrics()
        # get_other_info_sys_metrics()
        # get_sensor_metrics()

        time.sleep(interval)


def main():
    """Get list of all metrics.
    """
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
