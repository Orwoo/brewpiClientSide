import socket
import json

HOST = '85.214.88.34'
PORT = 65432


def request_value():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"REQUEST_VALUE")
        data = s.recv(1024)
        with open('client_data.json', 'w') as file:
            json.dump({"value": int(data.decode())}, file)


def send_values(value1, value2):
    data = {"value1": value1, "value2": value2}
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(json.dumps(data).encode())


def wrap_into_json(data):
    """Function to convert Python dictionary into JSON"""
    return json.dumps(data)


def get_timestamp():
    date_time = datetime.fromtimestamp(time())
    return date_time.strftime("%d-%m-%Y, %H:%M:%S")


def main():
    # For demonstration, let's request a value and then send two values
    request_value()
    send_values(42, 99)


if __name__ == "__main__":
    main()
