import json
import socket
from datetime import datetime
from time import sleep, time
from modules.temperature import get_sensor_temp, get_temp_set, write_temp_set_to_file

HOST = '85.214.88.34'
PORT = 5000


def get_timestamp():
    date_time = datetime.fromtimestamp(time())
    return date_time.strftime("%d-%m-%Y,%H:%M:%S")


def client_server_communication():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Trying to connect")
        counter_try = 1
        while True:
            try:
                s.connect((HOST, PORT))
                break
            except ConnectionRefusedError:
                print(f"Connection to {HOST} refused. Retry in 5 sec.({counter_try})")
                counter_try+=1
                sleep(5)

        while True:
            try:
                inner, outer = get_sensor_temp()
                temp_dump = {"time": get_timestamp(), "temp_inner": inner, "temp_outer": outer, "temp_set": get_temp_set().split(",")[0]}

                # send data
                try:
                    s.sendall(json.dumps(temp_dump).encode())
                except BrokenPipeError:
                    break

                # receive data
                data = s.recv(1024).decode()
                print('Received:', data)
                if data != get_temp_set():
                    write_temp_set_to_file(data)

            except (ValueError, FileNotFoundError):
                print("Error reading or parsing the JSON file.")
            sleep(5)

if __name__ == "__main__":
    client_server_communication()
