from time import time
from datetime import datetime
from modules.connect_tapo_plugs import *

heater = None
filename = "./src/config.json"
config = read_config(filename)


def wrap_into_json(data):
    """Function to convert Python dictionary into JSON"""
    return json.dumps(data)


def get_timestamp():
    date_time = datetime.fromtimestamp(time())
    return date_time.strftime("%d-%m-%Y, %H:%M:%S")


if __name__ == '__main__':
    pass
