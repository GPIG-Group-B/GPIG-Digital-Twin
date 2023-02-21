import json
import socket
import time
INIT_STRING = "GPIG-Group-B".encode()

def setup_server_connction(ip, port, num_connections=1):
    with socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM) as s:
        try:
            s.bind((ip, port))
        except OSError as e:
            print(f"Got error {e}. Retrying in 3 seconds")
            time.sleep(3)
        print(f"Waiting for connection on IP : {ip} | PORT : {port}")
        s.listen(num_connections)
        connection, _ = s.accept()
        print(f"Accepted connection on IP : {ip} | PORT : {port}")
        data, additional_data = receive_data(connection=connection,
                                             length=len(INIT_STRING))
        if data != INIT_STRING:
            print(f"Expected init string : {INIT_STRING}. Received {data} Closing connection")
            connection.close()
        else:
            print("Received expected init string. Accepting connection")
    return connection, additional_data

def send_json_message(connection : socket.socket, message_dict : dict, message_id : int):
    connection.sendall(message_id.to_bytes(length=2, byteorder="big"))
    data = json.dumps(message_dict).encode()
    connection.sendall(len(data).to_bytes(length=2, byteorder="big"))
    connection.sendall(data)

def send_device_type_id(connection : socket.socket, device_type_id : int):
    connection.sendall((device_type_id).to_bytes(length=2, byteorder="big"))


def receive_data(connection, length, data=b""):
    while len(data) < length:
        data += connection.recv(length - len(data))
        if not data:
            raise Exception("Connection was closed")
    return data[:length], data[length:]
