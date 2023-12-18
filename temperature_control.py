from modules.connect_tapo_plugs import read_config, get_credentials, connect_to_p100
from modules.temperature import get_sensor_temp, get_temp_set
from time import sleep


filename = "src/config.json"
config = read_config(filename)

sleep_while_regulation = 6
sleep_until_next_measure = 120

def init_cooler_and_heater():
    if config:
        while True:
            try:
                cooler_creds = get_credentials(config, "cooler")
                _cooler = connect_to_p100(cooler_creds['ip'], cooler_creds['email'], cooler_creds['pw'])

                heater_creds = get_credentials(config, "heater")
                _heater = connect_to_p100(heater_creds['ip'], heater_creds['email'], heater_creds['pw'])
                return [_cooler, _heater]
            except Exception as e:
                print("Connecting Tapos failed. Retry in 5s")
                print(e)
                sleep(5)
                continue


def exception_handling_plugs(plug_function):
    while True:
        try:
            plug_function
            break
        except Exception as e:
            global cooler, heater
            print("Error while regulating. Connection lost? Trying to reconncet in 5s.")
            sleep(5)
            cooler, heater = init_cooler_and_heater()
            print(f"exception_handling_plugs:\n{e}")


def control_temp():
    global cooler, heater
    inner, outer = get_sensor_temp()
    temp_set, th_set, th_outer, controller_state = get_temp_set().split(",")
    temp_set = float(temp_set)
    th_set = float(th_set)
    th_outer = float(th_outer)

    if not (temp_set - th_set <= inner <= temp_set + th_set):
        if inner < temp_set - th_set:
            while inner < temp_set - th_set and outer < inner + th_outer:
                inner, outer = get_sensor_temp()
                # the heat is on
                exception_handling_plugs(heater.turnOn())

                print("now heating")
                print(f"inner: {inner}, outer: {outer}, set: {temp_set}")
                if inner > outer + th_outer:
                    heater.turnOff()
                    print("too hot")
                    return
                sleep(sleep_while_regulation)
            heater.turnOff()
            print(f"target temp reached. inner: {inner}, set: {temp_set}")
        else:
            while inner > temp_set + th_set and outer > inner - th_outer:
                inner, outer = get_sensor_temp()
                # now cooling
                exception_handling_plugs(cooler.turnOn())
                print("now cooling")
                print(f"inner: {inner}, outer: {outer}, set: {temp_set}")
                if inner < outer - th_outer:
                    cooler.turnOff()
                    print("too cold")
                    return
                sleep(sleep_while_regulation)
            cooler.turnOff()
            print(f"target temp reached. inner: {inner}, set: {temp_set}")
    else:
        print("That's the way, aha, aha, i like it")


if __name__ == "__main__":
    while True:
        try:
            cooler, heater = init_cooler_and_heater()
            break
        except Exception as e:
            print("Init of power plugs failed. Are they connected? Retry in 5s.")
            print(f"Main loop:\n{e}")
            sleep(5)

    while True:
        control_temp()
        sleep(sleep_until_next_measure)
