from w1thermsensor import W1ThermSensor

# Initialize the sensors
sensors = W1ThermSensor.get_available_sensors()


def get_sensor_temp():
    sensors_temp = []
    for index, sensor in enumerate(sensors):
        # Get the temperature from the sensor
        temperature_in_celsius = sensor.get_temperature()
        sensors_temp.append(round(temperature_in_celsius, 2))
        # name = "inner" if "0b2280a" in sensor.id else "outer"
        # print("Sensor %s has temperature %.2f" % (name, temperature_in_celsius))
    return sensors_temp
