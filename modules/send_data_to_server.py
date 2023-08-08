import json
import socket
from datetime import datetime
from random import randint
from time import sleep, time


HOST = '85.214.88.34'
PORT = 5000


def send_to_server(ip, port, json_data):
    """Function to send JSON data to a server"""

    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    sock.connect((ip, port))

    try:
        # Send data
        sock.sendall(json_data.encode('utf-8'))
        print("Data sent to the server.")
    finally:
        # Close the connection
        sock.close()
        print("Socket closed.")


def wrap_into_json(data):
    """Function to convert Python dictionary into JSON"""
    return json.dumps(data)


def get_timestamp():
    date_time = datetime.fromtimestamp(time())
    return date_time.strftime("%d-%m-%Y, %H:%M:%S")


data = {
    "time": get_timestamp(),
    "temperature": randint(0, 100),
    "humidity": randint(40, 100),
    "pressure": randint(990, 1100)
}


while True:
    json_data = wrap_into_json(data)
    send_to_server(HOST, PORT, json_data)
    sleep(10)
