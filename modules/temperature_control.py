from time import sleep
from modules.temperature import get_sensor_temp
from modules.connect_tapo_plugs import read_config, get_credentials, connect_to_p100

filename = "../src/config.json"
config = read_config(filename)


def init_cooler_and_heater():
    if config:
        cooler_creds = get_credentials(config, "cooler")
        _cooler = connect_to_p100(cooler_creds['ip'], cooler_creds['email'], cooler_creds['pw'])

        heater_creds = get_credentials(config, "heater")
        _heater = connect_to_p100(heater_creds['ip'], heater_creds['email'], heater_creds['pw'])
        return [_cooler, _heater]


def control_temp(temp_set, th_outer=2, th_set=1):
    cooler, heater = init_cooler_and_heater()
    inner, outer = get_sensor_temp()

    if inner not in range(temp_set - th_set, temp_set + th_set):
        if inner < temp_set - th_set:
            while inner < temp_set - th_set and outer < inner + th_outer:
                inner, outer = get_sensor_temp()
                # the heat is on
                heater.turnOn()
                print("now heating")
                print(f"inner: {inner}, outer: {outer}, set: {temp_set}")  # TODO: temp logging here?
                if inner > outer + th_outer:
                    heater.turnOff()
                    print("too hot")
                    return
                sleep(1)
            heater.turnOff()
            print(f"target temp reached. inner: {inner}, set: {temp_set}")
        else:
            while inner > temp_set+th_set and outer > inner - th_outer:
                inner, outer = get_sensor_temp()
                # now cooling
                cooler.turnOn()
                print("now cooling")
                print(f"inner: {inner}, outer: {outer}, set: {temp_set}")
                if inner < outer - th_outer:
                    cooler.turnOff()
                    print("too cold")
                    return
                sleep(1)
            cooler.turnOff()
            print(f"target temp reached. inner: {inner}, set: {temp_set}")
    else:
        print("That's the way, aha, aha, i like it")


control_temp(18)


# TODO: get temp_set from file