import json
import socket
import threading
import multiprocessing
import time

from connection_utils import receive_data, receive_json, send_json_message


class TCPWorker(multiprocessing.Process):

    def __init__(self, ip="localhost", port=65432):
        self._ip = ip
        self._port = port
        self._close_connection_flag = multiprocessing.Event()
        self._additional_data = b""
        self.connection = True
        super().__init__()

    def run(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Connecting using IP : {self._ip} | PORT : {self._port}")
        while True:
            try:
                self.connection.connect((self._ip, self._port))
                break
            except Exception as e:
                print(e)
                print("Connection refused. Trying again in 3 seconds")
                time.sleep(3)
        print(f"Accepted connection on IP : {self._ip} | PORT : {self._port}")
        self.connection.sendall("GPIG-Group-B".encode())

        self._device_type_id, self._additional_data = receive_data(connection=self.connection,
                                                                   length=2,
                                                                   data=self._additional_data)
        self._device_type_id = int.from_bytes(self._device_type_id, byteorder="big")

        while True:
            json_data, self._additional_data, message_id = receive_json(connection=self.connection,
                                                                   additional_data=self._additional_data)
            print(f"Received message of type : {message_id}")
            print(f"Json received : {json_data}")
            if message_id == 0:
                send_json_message(connection=self.connection,
                                  message_dict={},
                                  message_id=message_id)



