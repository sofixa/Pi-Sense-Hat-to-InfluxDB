#!/usr/bin/python

import argparse
from sense_hat import SenseHat
from influxdb import InfluxDBClient


#send the data to InfluxDB
def send_to_influx(host, port, user, password, database, room, house, data):
	client = InfluxDBClient(host, port, user, password, database)
	json_body = [
		{
			"measurement": "sensors",
			"tags": {
				"room": room,
				"house": house
			},
			"fields": {
				"temperature": data['temperature'],
				"pressure": data['pressure'],
				"humidity": data['humidity']
			}
		}
	]
	print(client.write_points(json_body))


#get temp, pressure, humidity from the Sense HAT
def get_sensors(precision):
	sense = SenseHat()
	data = {}
	data['temperature'] = round(sense.get_temperature(), precision)
	data['pressure'] = round(sense.get_pressure(), precision)
	data['humidity'] = round(sense.get_humidity(), precision)
	return data
	

def parse_args():
	parser = argparse.ArgumentParser(description='example code to play with InfluxDB')
	parser.add_argument('--host', type=str, required=False, default='localhost', help='Hostname/IP of the InfluxDB server. Default localhost')
	parser.add_argument('--port', type=int, required=False, default=8086, help='Port of InfluxDB http API. Default 8086')
	parser.add_argument('--user', type=str, required=False, default='user', help='User to use for the InfluxDB connection. By default not needed')
        parser.add_argument('--password', type=str, required=False, default='password', help='User to use for the InfluxDB connection. By default not needed')
	parser.add_argument('--house', type=str, required=False, default='My House', help='Name of the house/appartment to serve as an InfluxDB tag name. Optional, default My House')
        parser.add_argument('--room', type=str, required=True, help='Name of the room to serve as an InfluxDB tag name. Required')
	parser.add_argument('--precision', type=int, required=False, default='2', help='Decimal point round precision, e.g. with 3 the results will be 24.054. Default 2')
	return parser.parse_args()


if __name__ == '__main__':
	args = parse_args()
	sensors = get_sensors(precision=args.precision)
	send_to_influx(host=args.host, port=args.port, user=args.user, password=args.password, database=args.database, room=args.room, house=args.house)

