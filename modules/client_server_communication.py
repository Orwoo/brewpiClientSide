import json
import socket
from time import sleep

HOST = '85.214.88.34'
PORT = 5000


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            try:

                dummy_temps = {"time": "23.03.23 9:15", "temp_inner": 25.3, "temp_outer": 24.0, "temp_set": 25.0}

                # with open('../src/sensor_temp.json', 'r') as f:
                #     data_json = json.load(f)

                s.sendall(json.dumps(dummy_temps).encode())

                data = s.recv(1024)
                print('Received:', data.decode())

                with open('../src/temp_set', 'w') as f:
                    f.write(data.decode())
                print("new temp_set written")

            except (ValueError, FileNotFoundError):
                print("Error reading or parsing the JSON file.")
            sleep(2)


if __name__ == "__main__":
    main()
