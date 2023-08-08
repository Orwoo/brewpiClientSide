import socket


def send_to_server(ip, port, json_data):
    """Function to send JSON data to a server"""

    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    sock.connect((ip, port))

    try:
        # Send data
        sock.sendall(json_data.encode('utf-8'))
        print("Data sent to the server.")
    finally:
        # Close the connection
        sock.close()
        print("Socket closed.")
