from w1thermsensor import W1ThermSensor

# Initialize the sensors
sensors = W1ThermSensor.get_available_sensors()
sensors_temp = {"inner": 0, "outer": 0}


def get_sensor_temp():
    for sensor in sensors:
        # Get the temperature from the sensor
        temperature_in_celsius = sensor.get_temperature()
        name = "inner" if "0b2280a" in sensor.id else "outer"
        sensors_temp[name] = round(temperature_in_celsius, 2)
        print("Sensor %s has temperature %.2f" % (name, temperature_in_celsius))
    return sensors_temp


# def measure_loop_endless(sleep_time):
#     while True:
#         get_sensor_temp()
#         sleep(sleep_time)


def set_temperature():
    pass
