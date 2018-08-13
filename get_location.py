#
# Copyright (C) 2018 Giuliano Pasqualotto (github.com/giulianopa)
# This code is licensed under MIT license (see LICENSE.txt for details)
#
import platform
import datetime
import geocoder
import decimal
import socket
import boto3
import time
import json


def get_location():
    """ Get current GPS location, using geocoder
    """

    g = geocoder.ip('me')
    return g.latlng


def get_utc_time():
    """ Get current time in UTC.
    """

    ts = time.time()
    return str(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == "__main__":
    location = get_location()
    time = get_utc_time()
    hostname = str(socket.gethostname())
    plat = platform.platform()

    # Connect to dynamodb
    client = boto3.client('dynamodb')

    # Create JSON
    data = {'time': {'S': time}, 'hostname': {'S': hostname},\
        'location': {'SS': [ str(location[0]), str(location[1]) ]},\
        'platform': {'S': plat}}

    # Update table
    response = client.put_item(TableName='DevLocation', Item=data)
    print(json.dumps(response, indent=4))
