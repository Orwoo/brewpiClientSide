from time import sleep
from w1thermsensor import W1ThermSensor

# Initialize the sensors
sensors = W1ThermSensor.get_available_sensors()


def get_sensor_temp():
    sensors_temp = []
    for index, sensor in enumerate(sensors):
        # Get the temperature from the sensor
        while True:
            try:
                temperature_in_celsius = sensor.get_temperature()
                sensors_temp.append(round(temperature_in_celsius, 2))
                break
            except Exception:
                print("Trying to get sensor data in 5s.")
                sleep(5)
        # name = "inner" if "0b2280a" in sensor.id else "outer"
        # print("Sensor %s has temperature %.2f" % (name, temperature_in_celsius))
    return sensors_temp


def get_temp_set():
    with open("../src/temp_set", "r") as f:
        try:
            return f.readlines()[1]
        except IndexError:
            print("reading temp_set failed. Couldn't find any values")
            print("setting temp_set to 15,1,1")
            return "15,1,1"


def write_temp_set_to_file(_data):
    if _data:
        with open('../src/temp_set', 'w') as f:
            print(f"writing new temperatures: {_data}")
            f.write("temp_set,threshold_set,threshold_outer\n")
            f.write(_data)
    else:
        print("No data found. Nothing written")