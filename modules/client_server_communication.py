import json
import smtplib
import requests
from email.message import EmailMessage
from time import sleep, time
from modules.temperature import get_sensor_temp, get_temp_set, write_temp_set_to_file
import socket
from datetime import datetime

SERVER_URL = 'http://192.168.188.20:5000/brewpi'
# HOST = '85.214.88.34'
# PORT = 5000


# def get_timestamp():
#     date_time = datetime.fromtimestamp(time())
#     return date_time.strftime("%d-%m-%Y,%H:%M:%S")


# def client_server_communication():
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         print("Trying to connect")
#         counter_try = 1
#         while True:
#             try:
#                 s.connect((HOST, PORT))
#                 break
#             except ConnectionRefusedError:
#                 print(f"Connection to {HOST} refused. Retry in 5 sec.({counter_try})")
#                 counter_try+=1
#                 sleep(5)
#
#         while True:
#             try:
#                 inner, outer = get_sensor_temp()
#                 temp_dump = {"time": get_timestamp(), "temp_inner": inner, "temp_outer": outer, "temp_set": get_temp_set().split(",")[0]}
#
#                 # send data
#                 try:
#                     s.sendall(json.dumps(temp_dump).encode())
#                 except BrokenPipeError:
#                     break
#
#                 # receive data
#                 data = s.recv(1024).decode()
#                 print('Received:', data)
#                 if data != get_temp_set():
#                     write_temp_set_to_file(data)
#
#             except (ValueError, FileNotFoundError):
#                 print("Error reading or parsing the JSON file.")
#             sleep(5)


def send_email(error):
    with open("../src/config.json") as f:
        data = json.load(f)
    msg = EmailMessage()
    msg.set_content(f"Your Flask app on your server has crashed.\nHere is the error msg:\n\n"
                    f"{error}")
    msg['Subject'] = 'fermPi server app crashed'
    msg['From'] = data['mail']['from']
    msg['To'] = data['mail']['to']

    # Establish a connection to your SMTP server
    with smtplib.SMTP(data['mail']['smtp_server'], data['port']) as server:
        server.starttls()
        server.login(data['mail']['from'], data['mail']['password'])
        server.send_message(msg)

def send_temperature_data(temp_inner, temp_outer, temp_set):
    data = {
        'temp_inner': temp_inner,
        'temp_outer': temp_outer,
        'temp_set': temp_set
    }
    response = requests.post(f"{SERVER_URL}/temp-client", json=data)
    print(response.json())


def get_temp_set_from_server():
    response = requests.get(f"{SERVER_URL}/get-set-temp")
    try:
        data = response.content.decode()
        print(f"RESPONSE: {data}")
        if data != get_temp_set():
            write_temp_set_to_file(data)

        return data

    except Exception as e:
        send_email(e)
        return "Getting temp_set failed"


def client_server_communication_loop():
    while True:
        inner, outer = get_sensor_temp()
        send_temperature_data(temp_inner=inner, temp_outer=outer, temp_set=get_temp_set().split(",")[0])
        temp_set_value = get_temp_set_from_server()
        print(f"Temp Set: {temp_set_value}")
        sleep(60)


if __name__ == "__main__":
    client_server_communication_loop()

# TODO: separate projects
