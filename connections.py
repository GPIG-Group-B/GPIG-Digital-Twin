import multiprocessing
import socket
import threading
import multiprocessing


def receive_data(connection, length, data=b""):
    while len(data) < length:
        data += connection.recv(length - len(data))
        if not data:
            raise Exception("Connection was closed")
    return data[:length], data[length:]

class TCPWorker(multiprocessing.Process):

    def __init__(self, ip="localhost", port=65432):
        super().__init__()
        self._ip = ip
        self._port = port


        self._close_connection_flag = multiprocessing.Event()

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self._ip, self._port))
            print(f"Waiting for connection on IP : {self._ip} | PORT : {self._ip}")
            s.listen(1)
            connection, _ = s.accept()
            print(f"Accepted connection on IP : {self._ip} | PORT : {self._ip}")

        sender_worker = TCPSenderWorker(connection=connection, connection_close_flag=self._close_connection_flag)
        receiver_worker = TCPReceiverWorker(connection=connection, connection_close_flag=self._close_connection_flag)
        sender_worker.run()
        receiver_worker.run()
        sender_worker.join()
        receiver_worker.join()
        connection.shutdown(socket.SHUT_RDWR)
        connection.close()










class TCPSenderWorker(threading.Thread):

    def __init__(self, connection : socket.socket, connection_close_flag):
        super().__init__()
        self._connection = connection
        self._connection_close_flag = connection_close_flag
        print("Initialised TCP Sender Worker")

    def run(self):
        n = 0
        while True:
            n += 1
            if self._connection_close_flag.is_set():
                print("Connection closed")
                break
            self._connection.sendall(str.encode(str(n)))


class TCPReceiverWorker(threading.Thread):

    def __init__(self, connection : socket.socket, connection_close_flag : multiprocessing.Event):
        super().__init__()
        self._connection = connection
        self._connection_close_flag = connection_close_flag
        print("Initialised TCP Receiver Worker")

    def run(self):
        existing_data = b""
        while True:
            data_received, existing_data = receive_data(self._connection, length=1024, data=existing_data)
            print(data_received)
            if data_received == str.encode("E"):
                self._connection_close_flag.set()
                break




