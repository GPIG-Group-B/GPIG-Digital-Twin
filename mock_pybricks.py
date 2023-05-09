import threading
from queue import Queue

import constants
from connection_utils import setup_server_connection, send_json_message, send_device_type_id, receive_json, setup_client_connection
import socket
from collections import OrderedDict
class Direction:

    COUNTERCLOCKWISE = "COUNTERCLOCKWISE"
    CLOCKWISE = "clockwise"

class PybricksDevice:

    def __init__(self, port, device_type_id):
        self._port, self._additional_data = setup_server_connection(ip=port.ip,
                                                                    port = port.port,
                                                                    num_connections=1)
        self._DEVICE_TYPE_ID = device_type_id
        send_device_type_id(connection=self._port, device_type_id=self._DEVICE_TYPE_ID)

    def _send_info_message(self):
        MESSAGE_ID = 1
        EXCLUDE_FROM_INFO_MESSAGE = ["_port", "_additional_data", "_DEVICE_TYPE_ID"]
        self.send_message(data=vars(self),
                          exclusions=EXCLUDE_FROM_INFO_MESSAGE,
                          message_id=MESSAGE_ID)

    def send_message(self, data : dict, message_id : int, exclusions = None, expect_response = True):
        data = {key.strip("_") : val for key,val in data.items() if key not in exclusions}
        send_json_message(connection=self._port,
                          message_dict=data,
                          message_id=message_id)
        if expect_response:
            json_data, self._additional_data, received_message_id = receive_json(connection=self._port,
                                                                                   additional_data=self._additional_data)
            if received_message_id != message_id:
                raise ValueError(f"Message ID : {message_id}. Received message id back of {received_message_id}")
            return json_data
        else:
            return None

    def send_shutdown_message(self):
        MESSAGE_ID = 0
        print("Sending shutdown message")
        self.send_message(data={}, message_id=MESSAGE_ID, expect_response=False)
        print("Shutting down socket")
        self._port.shutdown(socket.SHUT_RDWR)
        print("Closing down socket")
        self._port.close()
        print("Completed socket close")


class Motor(PybricksDevice):

    def __init__(self,
                 port: dict,
                 positive_direction: Direction,
                 gears : list = None,
                 reset_angle: bool = False):
        super().__init__(port,
                         device_type_id=0)
        print("Finished setup of port")
        self._positive_direction = positive_direction
        self._gears = gears
        self._reset_angle = reset_angle
        self._speed = 0
        self._angle = 0
        self._load = "unknown"
        self._ongoing_command = False
        self._send_info_message()

    def speed(self):
        return self._speed

    def angle(self):
        MESSAGE_ID = 10
        return_message = self.send_message(data={},
                 message_id=MESSAGE_ID)
        return return_message["angle"]

    def reset_angle(self, angle : int):
        self._angle = angle

    def stop(self):
        MESSAGE_ID = 2
        self._ongoing_command = True
        self.send_message(data={},
                          message_id=MESSAGE_ID)
        self._ongoing_command = False


    def brake(self):
        MESSAGE_ID = 3
        self._ongoing_command = True
        self.send_message(data={},
                          message_id=MESSAGE_ID)
        self._ongoing_command = False

    def hold(self):
        MESSAGE_ID = 4
        self._ongoing_command = True
        self.send_message(data={},
                          message_id=MESSAGE_ID)
        self._ongoing_command = False

    def run(self, speed : int):
        MESSAGE_ID = 5
        self._ongoing_command = True
        self.send_message(data=locals(),
                          exclusions=["self", "MESSAGE_ID"],
                          message_id=MESSAGE_ID)
        self._ongoing_command = False

    def run_time(self, speed : int, time : int, then = None, wait = True):
        MESSAGE_ID = 6
        self._ongoing_command = True
        self.send_message(data=locals(),
                          exclusions=["self", "MESSAGE_ID"],
                          message_id=MESSAGE_ID)
        self._ongoing_command = False

    def run_angle(self, speed : int, rotation_angle : int, then = None, wait=True):
        MESSAGE_ID = 7
        self._ongoing_command = True
        self.send_message(data=locals(),
                          exclusions=["self", "MESSAGE_ID"],
                          message_id=MESSAGE_ID)
        self._ongoing_command = False

    def run_target(self,
                   speed : int,
                   target_angle : int,
                   then = None,
                   wait : bool = True):
        MESSAGE_ID = 8
        self._ongoing_command = True
        self.send_message(data=locals(),
                          exclusions=["self", "MESSAGE_ID"],
                          message_id=MESSAGE_ID)
        self._ongoing_command = False

    def track_target(self,
                     target_angle : int):
        MESSAGE_ID = 9
        self._ongoing_command = True
        self.send_message(data=locals(),
                          exclusions=["self", "MESSAGE_ID"],
                          message_id=MESSAGE_ID)
        self._ongoing_command = False

    def run_until_stalled(self):
        raise NotImplementedError()

    def done(self):
        return self._ongoing_command


class DriveBase():

    def __init__(self,
                 left_motor : Motor,
                 right_motor : Motor,
                 wheel_diameter : int,
                 axle_track : int,
                 positive_direction : Direction):
        self._left_motor = left_motor
        self._right_motor = right_motor
        self._wheel_diameter = wheel_diameter
        self._axle_track = axle_track
        self._positive_direction = positive_direction
        self._ongoing_command = False

    def straight(self,
                 distance : int,
                 then=None,
                 wait : bool =True):
        MESSAGE_ID = 2
        self._left_motor.run(55)
        self._right_motor.run(55)

    def turn(self,
             angle : int,
             then=None,
             wait : bool =True):
        MESSAGE_ID = 3
        self._ongoing_command = True
        self._left_motor.send_message(data=locals(),
                          exclusions=["self", "MESSAGE_ID"],
                          message_id=MESSAGE_ID)
        self._right_motor.send_message(data=locals(),
                          exclusions=["self", "MESSAGE_ID"],
                          message_id=MESSAGE_ID)
        self._ongoing_command = False

    def curve(self,
              radius : int,
              angle : int,
              then=None,
              wait : bool =True):
        MESSAGE_ID = 4
        self._ongoing_command = True
        self._left_motor.send_message(data=locals(),
                          exclusions=["self", "MESSAGE_ID"],
                          message_id=MESSAGE_ID)
        self._right_motor.send_message(data=locals(),
                          exclusions=["self", "MESSAGE_ID"],
                          message_id=MESSAGE_ID)
        self._ongoing_command = False

    def drive(self,
              speed : int,
              turn_rate : int):
        MESSAGE_ID = 5
        self._ongoing_command = True
        self._left_motor.send_message(data=locals(),
                          exclusions=["self", "MESSAGE_ID"],
                          message_id=MESSAGE_ID)
        self._right_motor.send_message(data=locals(),
                          exclusions=["self", "MESSAGE_ID"],
                          message_id=MESSAGE_ID)
        self._ongoing_command = False


    def stop(self):
        MESSAGE_ID = 6
        self._ongoing_command = True
        self._left_motor.send_message(data=locals(),
                          exclusions=["self", "MESSAGE_ID"],
                          message_id=MESSAGE_ID)
        self._right_motor.send_message(data=locals(),
                          exclusions=["self", "MESSAGE_ID"],
                          message_id=MESSAGE_ID)
        self._ongoing_command = False

    def distance(self):
        raise NotImplementedError()

    def angle(self):
        raise NotImplementedError()

    def state(self):
        raise NotImplementedError()

    def reset(self):
        raise NotImplementedError()


    def settings(self,
                 straight_speed : int = None,
                 straight_acceleration : int = None,
                 turn_rate : int = None,
                 turn_acceleration : int = None):
        raise NotImplementedError()

    def done(self):
        return self._ongoing_command


class UltrasonicSensor(PybricksDevice):
    def __init__(self,
                 port):
        super().__init__(port=port,
                         device_type_id=1)
        self.light = Light()

    def distance(self):
        MESSAGE_ID = 2
        response_message = self.send_message(data=locals(),
                                             exclusions=["self", "MESSAGE_ID"],
                                             message_id=MESSAGE_ID)
        return response_message["distance"]

    def presence(self):
        MESSAGE_ID = 3
        response_message = self.send_message(data=locals(),
                                             exclusions=["self", "MESSAGE_ID"],
                                             message_id=MESSAGE_ID)
        return response_message["presence"]

 
class Light():

    def on(self, brightness : int):
        print("Warning : Lights on is not implemented")

    def off(self):
        print("Warning : Lights off is not implemented")

class ColorSensor(PybricksDevice):

    def __init__(self,
                 port):
        super().__init__(port=port,
                         device_type_id=2)

    def color(self, surface : bool = True):
        MESSAGE_ID = 2
        response_message = self.send_message(data=locals(),
                                             exclusions=["self", "MESSAGE_ID"],
                                             message_id=MESSAGE_ID)
        return response_message["colour"]

    def reflection(self):
        MESSAGE_ID = 3
        response_message = self.send_message(data=locals(),
                                             exclusions=["self", "MESSAGE_ID"],
                                             message_id=MESSAGE_ID)
        return response_message["reflection"]

    def ambient(self):
        MESSAGE_ID = 4
        response_message = self.send_message(data=locals(),
                                             exclusions=["self", "MESSAGE_ID"],
                                             message_id=MESSAGE_ID)
        return response_message["ambient_light"]


class ForceSensor(PybricksDevice):

    def __init__(self,
                 port):
        super().__init__(port=port,
                         device_type_id=3)

    def force(self):
        MESSAGE_ID = 2
        response_message = self.send_message(data=locals(),
                                             exclusions=["self", "MESSAGE_ID"],
                                             message_id=MESSAGE_ID)
        return response_message["force"]

    def distance(self):
        MESSAGE_ID = 3
        response_message = self.send_message(data=locals(),
                                             exclusions=["self", "MESSAGE_ID"],
                                             message_id=MESSAGE_ID)
        return response_message["distance"]

    def pressed(self, force : int = 3):
        MESSAGE_ID = 4
        response_message = self.send_message(data=locals(),
                                             exclusions=["self", "MESSAGE_ID"],
                                             message_id=MESSAGE_ID)
        return response_message["is_pressed"]

    def touched(self):
        MESSAGE_ID = 5
        response_message = self.send_message(data=locals(),
                                             exclusions=["self", "MESSAGE_ID"],
                                             message_id=MESSAGE_ID)
        return response_message["touched"]


class ColorDistanceSensor(PybricksDevice):

    def __init__(self,
                 port):
        super().__init__(port=port,
                         device_type_id=4)
        self.light = Light()

    def color(self, surface : bool = True):
        MESSAGE_ID = 2
        response_message = self.send_message(data=locals(),
                                             exclusions=["self", "MESSAGE_ID"],
                                             message_id=MESSAGE_ID)
        return response_message["colour"]

    def reflection(self):
        MESSAGE_ID = 3
        response_message = self.send_message(data=locals(),
                                             exclusions=["self", "MESSAGE_ID"],
                                             message_id=MESSAGE_ID)
        return response_message["reflection"]

    def ambient(self):
        MESSAGE_ID = 4
        response_message = self.send_message(data=locals(),
                                             exclusions=["self", "MESSAGE_ID"],
                                             message_id=MESSAGE_ID)
        return response_message["ambient_light"]


    def distance(self):
        MESSAGE_ID = 5
        response_message = self.send_message(data=locals(),
                                             exclusions=["self", "MESSAGE_ID"],
                                             message_id=MESSAGE_ID)
        return response_message["distance"]


class Broadcast:

    def __init__(self, topics : list, connection : socket.socket, additional_data = b""):
        self._topics = topics
        self._inbound_queue = Queue()
        self._outbound_queue = Queue()
        self._additional_data = additional_data
        self._connection = connection
        self._known_types = {"int" : int,
                             "str" : str,
                             "float" : float,
                             "bool" : bool}
        self._receiver_thread = threading.Thread(target=self.receiver_worker_function)
        self._sender_thread = threading.Thread(target=self.sender_worker_function)
        self._receiver_thread.start()
        self._sender_thread.start()

    def join(self):
        self._sender_thread.join()
        self._receiver_thread.join()



    def sender_worker_function(self):
        while True:
            data_dict = self._outbound_queue.get(block=True)
            if data_dict == "shutdown":
                return
            send_json_message(connection=  self._connection,
                              message_dict=data_dict,
                              message_id=0)

    def receiver_worker_function(self):
        while True:
            data, self._additional_data, message_type = receive_json(connection=self._connection,
                                                                     additional_data=self._additional_data)
            if data["topic"] == "shutdown":
                self._outbound_queue.put("shutdown")
                print("Received shutdown message type. Shutting down")
                return
            self._inbound_queue.put(data)

    def send(self, broadcast_data : list):
        topic = broadcast_data[0]
        data_to_send = broadcast_data[1:]
        if topic not in self._topics:
            raise ValueError(f"You have attempted to send on topic : {topic} but broadcast is setup with these topics : {self._topics}")
        data_dict = OrderedDict([(data, str(type(data))) for data in data_to_send])
        full_json = {"topic" : topic,
                     "data" : data_dict}
        self._outbound_queue.put(full_json)



    def receive(self, topic):
        if self._inbound_queue.empty():
            return None
        else:
            data = self._inbound_queue.get()
            topic_received = data["topic"]
            if topic_received != topic:
                #TODO: Figure out a better solution
                self._inbound_queue.put(data)
                return None
            else:
                return [self._known_types[each_key](each_var) for each_var, each_key in data["data"]]



class BroadcastHost(Broadcast):

    def __init__(self, topics):
        connection, additional_data = setup_server_connction(ip=constants.BROADCAST_IP,
                                                             port=constants.BROADCAST_PORT,
                                                             num_connections=1)

        super().__init__(topics = topics,
                         connection = connection,
                         additional_data = additional_data)


class BroadcastClient(Broadcast):

    def __init__(self, topics):
        connection, additional_data = setup_client_connction(ip=constants.BROADCAST_IP,
                                                             port = constants.BROADCAST_PORT)

        super().__init__(topics = topics,
                         connection = connection,
                         additional_data = additional_data)









