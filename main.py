import json
from random import randint
from time import sleep, time
from datetime import datetime
from modules.connect_tapo_plugs import *
from modules.temperature import *

heater = None
filename = "./src/config.json"
config = read_config(filename)


def wrap_into_json(data):
    """Function to convert Python dictionary into JSON"""
    return json.dumps(data)


def get_timestamp():
    date_time = datetime.fromtimestamp(time())
    return date_time.strftime("%d-%m-%Y, %H:%M:%S")


# Example usage:

# data = {
#     "time": get_timestamp(),
#     "temperature": randint(0, 100),
#     "humidity": randint(40, 100),
#     "pressure": randint(990, 1100)
# }


# def init_cooler_and_heater():
#     if config:
#         cooler_creds = get_credentials(config, "cooler")
#         _cooler = connect_to_p100(cooler_creds['ip'], cooler_creds['email'], cooler_creds['pw'])
#
#         heater_creds = get_credentials(config, "heater")
#         _heater = connect_to_p100(heater_creds['ip'], heater_creds['email'], heater_creds['pw'])
#         return _cooler, _heater


if __name__ == '__main__':
    # cooler, heater = init_cooler_and_heater()
    pass

    # while True:
    #     json_data = wrap_into_json(data)
    #     send_to_server('85.214.88.34', 5000, json_data)
    #     sleep(10)
