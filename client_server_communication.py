import requests
from time import sleep
from modules.temperature import get_sensor_temp, get_temp_set, write_temp_set_to_file
from modules.utility import is_process_running, kill_process_by_name, send_email, start_process

# SERVER_URL = 'https://85.214.88.34/fermpi'
SERVER_URL = 'http://192.168.188.20:5000/fermpi'

# time delay for re-run if exception
delay = 60


def send_temperature_data(temp_inner, temp_outer, temp_set, controller_state_client):
    data = {
        'temp_inner': temp_inner,
        'temp_outer': temp_outer,
        'temp_set': temp_set,
        'controller_state_client': controller_state_client
    }
    try:
        response = requests.post(f"{SERVER_URL}/temp-client", verify=False, json=data)
        print(response.json())
    except Exception as e:
        send_email(f"send_temperature_data:\n{e}")


def get_temp_set_from_server():
    response = requests.get(f"{SERVER_URL}/get-set-temp", verify=False)
    try:
        data = response.content.decode()
        print(f"RESPONSE: {data}")
        if data != get_temp_set():
            write_temp_set_to_file(data)

        return data

    except Exception as e:
        send_email(f"get_temp_set_from_server:\n{e}")
        return "Getting temp_set failed"


def client_server_communication_loop():
    while True:
        # send temp data to server
        try:
            inner, outer = get_sensor_temp()
            print(inner, outer)
            send_temperature_data(temp_inner=inner, temp_outer=outer, temp_set=get_temp_set().split(",")[0],
                                  controller_state_client=get_temp_set().split(",")[3])
        except Exception as e:
            send_email(f"client_server_communication_loop:\n{e}")
            print(f"Error while sending data. Pausing csc loop for {delay}s...")
            sleep(delay)
            continue

        # receive temps to set from server for temp control
        try:
            temp_set_value = get_temp_set_from_server()
            print(f"Temp Set: {temp_set_value}")

        except Exception as e:
            send_email(f"client_server_communication_loop:\n{e}")
            print(f"Error while receiving data. Pausing csc loop for {delay}s...")
            sleep(delay)
            continue

        print(get_temp_set().split(",")[3])
        if get_temp_set().split(",")[3] == "on":
            if not is_process_running("temperature_control.py"):
                start_process("temperature_control.py")
        else:
            if is_process_running("temperature_control.py"):
                kill_process_by_name("temperature_control.py")
        sleep(60)


if __name__ == "__main__":
    client_server_communication_loop()
