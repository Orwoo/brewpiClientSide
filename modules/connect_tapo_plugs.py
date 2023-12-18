import json
from PyP100 import PyP100
from time import sleep


def read_config(file):
    """Read configurations including credentials from a JSON file."""
    try:
        with open(file, 'r') as file:
            data = json.load(file)
            return data

    except json.JSONDecodeError as e:
        print("Error decoding JSON.")
        return None
    except FileNotFoundError as e:
        print(f"File '{file}' not found.")
        return None


def get_credentials(conf_file, user):
    """Retrieve credentials for specified users."""
    credentials_data = conf_file.get('credentials', {})

    result = {}

    if user in credentials_data:
        result["user"] = user
        result.update(credentials_data[user])
    else:
        print(f"No credentials found for {user}")

    return result


def connect_to_p100(ip, mail, pw):
    print("----------------")
    print(f"connecting P100 (ip: {ip})")
    p100 = PyP100.P100(ip, mail, pw)
    p100.handshake()
    p100.login()
    print("handshake and login: ok")
    print("toggle states")
    p100.toggleState()
    sleep(1)
    p100.toggleState()
    print("init done!")
    print("now turning plug off")
    sleep(1)
    p100.turnOff()
    return p100

# TODO: reconnect, if connection breaks
# TODO: connection loop and specific connection error. Maybe with logging