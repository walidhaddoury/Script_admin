import os

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import socket


class database:
    token = os.environ.get("INFLUXDB_TOKEN")
    org = "alexis.majchrzak77@gmail.com"
    url = "https://us-east-1-1.aws.cloud2.influxdata.com"
    bucket = "python_bdd"

    client = InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    query_api = client.query_api()
    point = None

    def set_point(self, point_name: str, field_name: str, value: float, tag_name: str = None, tag_value: str = None):
        if tag_name and tag_value:
            self.point = (
                Point(point_name)
                .tag(tag_name, tag_value)
                .tag("system", socket.gethostname())
                .field(field_name, float(value))
            )
        else:
            self.point = (
                Point(point_name)
                .tag("system", socket.gethostname())
                .field(field_name, float(value))
            )

    def send_metric(self):
        self.write_api.write(bucket=self.bucket, org=self.org, record=self.point)