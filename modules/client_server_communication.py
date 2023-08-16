import json
import socket
from datetime import datetime
from time import sleep, time
from modules.temperature import get_sensor_temp

HOST = '85.214.88.34'
PORT = 5000


def get_timestamp():
    date_time = datetime.fromtimestamp(time())
    return date_time.strftime("%d-%m-%Y,%H:%M:%S")


def get_temp_set():
    with open("../src/temp_set", "r") as f:
        return f.read()


def client_server_communication():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            try:
                inner, outer = get_sensor_temp()
                temp_dump = {"time": get_timestamp(), "temp_inner": inner, "temp_outer": outer, "temp_set": get_temp_set()}

                s.sendall(json.dumps(temp_dump).encode())

                data = s.recv(1024)
                print('Received:', data.decode())

                with open('../src/temp_set', 'w') as f:
                    f.write(data.decode())
                print("new temp_set written")

            except (ValueError, FileNotFoundError):
                print("Error reading or parsing the JSON file.")
            sleep(5)


if __name__ == "__main__":
    client_server_communication()


# TODO: get sensor temp
# TODO: write received temp_set to file
# TODO: write temp_set only if changed (more save?)