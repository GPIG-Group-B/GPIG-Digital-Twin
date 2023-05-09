import json
import socket
import time

ACKNOWLEDGEMENT_CONNECTION_STRING = "GPIG-Group-B-Server".encode()
INIT_CONNECTION_STRING = "GPIG-Group-B-Client".encode()



def setup_server_connection(ip,
                            port,
                            num_connections=1):
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
                                             length=len(INIT_CONNECTION_STRING))
        if data != INIT_CONNECTION_STRING:
            print(f"Expected init string : {INIT_CONNECTION_STRING}. Received {data} Closing connection")
            connection.close()
        else:
            print("Received expected init string. Accepting connection. Sending confirmation string")
            connection.sendall(ACKNOWLEDGEMENT_CONNECTION_STRING)
    return connection, additional_data

def setup_client_connection(ip,
                           port):
    with socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM) as s:
        try:
            s.connect((ip, port))
        except OSError as e:
            print(f"Got error {e}. Retrying in 3 seconds")
            time.sleep(3)
        print(f"Accepted connection on IP : {ip} | PORT : {port}")
        s.sendall(INIT_CONNECTION_STRING)
        data, additional_data = receive_data(connection=s,
                                             length=len(ACKNOWLEDGEMENT_CONNECTION_STRING))
        if data != INIT_CONNECTION_STRING:
            print(f"Expected init string : {ACKNOWLEDGEMENT_CONNECTION_STRING}. Received {data} Closing connection")
            s.close()
        else:
            print("Received expected init string. Accepting connection. Sending confirmation string")
    return s, additional_data


def send_json_message(connection: socket.socket,
                      message_dict: dict,
                      message_id: int):
    connection.sendall(message_id.to_bytes(length=2,
                                           byteorder="little"))
    data = json.dumps(message_dict).encode()
    connection.sendall(len(data).to_bytes(length=2,
                                          byteorder="little"))
    connection.sendall(data)


def send_device_type_id(connection: socket.socket,
                        device_type_id: int):
    connection.sendall((device_type_id).to_bytes(length=2,
                                                 byteorder="little"))


def receive_data(connection,
                 length,
                 data=b""):
    while len(data) < length:
        data += connection.recv(length - len(data))
        if not data:
            raise Exception("Connection was closed")
    return data[:length], data[length:]


def receive_json(connection: socket,
                 header_size : int=2,
                 additional_data : bytes =b""):
     message_type, additional_data = receive_data(connection=connection,
                                                 length=header_size,
                                                 data=additional_data)
     message_type = int.from_bytes(message_type, byteorder="little")
     message_length, additional_data = receive_data(connection=connection,
                                                   length=header_size,
                                                   data=additional_data)

     message_length = int.from_bytes(message_length,
                                    byteorder="little")
     json_data, additional_data = receive_data(connection=connection,
                                              length=message_length,
                                              data=additional_data)
     json_data = json.loads(json_data.decode())
     return json_data, additional_data, message_type
