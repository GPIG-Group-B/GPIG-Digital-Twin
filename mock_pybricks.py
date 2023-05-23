import math
import threading
import time
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
        return not self._ongoing_command


class DriveBase():

    def __init__(self,
                 left_motor : Motor,
                 right_motor : Motor,
                 wheel_diameter : int,
                 axle_track : int):
        self._left_motor = left_motor
        self._right_motor = right_motor
        self._wheel_diameter = wheel_diameter
        self._axle_track = axle_track
        self._ongoing_command = False

    def straight(self,
                 distance : int,
                 then=None,
                 wait : bool =True):
        MESSAGE_ID = 2
        speed_to_run = 35
        if distance < 0:
            speed_to_run *= -1
            distance = abs(distance)
        self._ongoing_command = True
        self._left_motor.run(speed_to_run)
        self._right_motor.run(speed_to_run)
        self._run_for_distance(distance=distance)
        self._ongoing_command = False

    def _run_for_distance(self, distance):
        left_motor_driven_distance, right_motor_driven_distance, avg_driven_distance = 0,0, 0
        left_motor_last_angle = self._left_motor.angle()
        right_motor_last_angle = self._right_motor.angle()
        left_motor_current_angle, right_motor_current_angle = left_motor_last_angle, right_motor_last_angle
        print(f"Average driven distance : {avg_driven_distance} | distance : {distance}")
        while avg_driven_distance < distance:
            print(f"Average driven distance : {avg_driven_distance}. {distance}")
            left_motor_driven_distance += self._get_distance_from_angle_diff(left_motor_last_angle, left_motor_current_angle)
            right_motor_driven_distance += self._get_distance_from_angle_diff(right_motor_last_angle, right_motor_current_angle)
            right_motor_last_angle = right_motor_current_angle
            left_motor_last_angle = left_motor_current_angle
            left_motor_current_angle = self._left_motor.angle()
            right_motor_current_angle = self._right_motor.angle()
            avg_driven_distance = (left_motor_driven_distance + right_motor_driven_distance) / 2
        print(f"Average driven distance : {avg_driven_distance}. {distance}")
        self._left_motor.stop()
        self._right_motor.stop()


    def _get_distance_from_angle_diff(self, last_angle, current_angle):
        return abs(((current_angle - last_angle)/ 360) * math.pi * self._wheel_diameter)


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
        speed_to_run = 35
        if radius < 0:
            speed_to_run *= -1
            radius = abs(radius)
        inner_radius = 2 * math.pi * (radius - (self._axle_track / 2)) * (angle / 360)
        outer_radius = 2 * math.pi * (radius + (self._axle_track / 2)) * (angle / 360)
        power_ratio = outer_radius / inner_radius
        print(f"Power ratio  {power_ratio}")
        print(f"Base speed : {speed_to_run} | Ratio speed : {int(speed_to_run * power_ratio)}")
        self._ongoing_command = True
        self._ongoing_command = True
        self._left_motor.run(speed_to_run)
        self._right_motor.run(int(speed_to_run * power_ratio))
        self._run_for_distance(distance=(inner_radius + outer_radius) / 2)
        self._ongoing_command = False
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
        self._left_motor.stop()
        self._right_motor.stop()
        # self._left_motor.send_message(data=locals(),
        #                   exclusions=["self", "MESSAGE_ID"],
        #                   message_id=MESSAGE_ID)
        # self._right_motor.send_message(data=locals(),
        #                   exclusions=["self", "MESSAGE_ID"],
        #                   message_id=MESSAGE_ID)
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
        return not self._ongoing_command


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
        self._colour_list = [Color.RED,
                             Color.YELLOW,
                             Color.GREEN,
                             Color.BLUE,
                             Color.WHITE,
                             Color.NONE]

    def color(self, surface : bool = True):
        MESSAGE_ID = 2
        response_message = self.send_message(data=locals(),
                                             exclusions=["self", "MESSAGE_ID"],
                                             message_id=MESSAGE_ID)

        return ColorHSV(**response_message)

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

    def detectable_colors(self, colour_list: list = None):
        if colour_list is None:
            return self._colour_list

        self._colour_list = colour_list


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
        return response_message["is_touched"]


class ColorDistanceSensor(PybricksDevice):

    def __init__(self,
                 port):
        super().__init__(port=port,
                         device_type_id=4)
        self._colour_list = [Color.RED,
                             Color.YELLOW,
                             Color.GREEN,
                             Color.BLUE,
                             Color.WHITE,
                             Color.NONE]
        self.light = Light()

    def color(self, surface : bool = True):
        MESSAGE_ID = 2
        response_message = self.send_message(data=locals(),
                                             exclusions=["self", "MESSAGE_ID"],
                                             message_id=MESSAGE_ID)

        return ColorHSV(**response_message)

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

    def detectable_colors(self, colour_list : list = None):
        if colour_list is None:
            return self._colour_list

        self._colour_list = colour_list


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
        print("Sender thread joined")
        self._sender_thread.join()
        print("REceived thread joined")
        self._receiver_thread.join()



    def sender_worker_function(self):
        while True:
            data_dict = self._outbound_queue.get(block=True)
            send_json_message(connection=  self._connection,
                              message_dict=data_dict,
                              message_id=0)
            if not self._receiver_thread.is_alive() or data_dict["topic"] == "shutdown":
                print("Shutting down sender worker")
                return

    def receiver_worker_function(self):
        while True:
            try:
                data, self._additional_data, message_type = receive_json(connection=self._connection,
                                                                         additional_data=self._additional_data)
            except socket.error:
                print("Caught connection closed. Initiating shutdown of workers")
                return
            self._inbound_queue.put(data)
            if not self._sender_thread.is_alive() or data["topic"] == "shutdown":
                print("Shutting down receiver worker")
                return

    def send(self, topic, broadcast_data : list):
        if type(broadcast_data) not in (list, tuple):
            broadcast_data = [broadcast_data]
        if topic not in self._topics:
            raise ValueError(f"You have attempted to send on topic : {topic} but broadcast is setup with these topics : {self._topics}")
        data_dict = OrderedDict([(f"value_{i}", (data, type(data).__name__)) for i, data in enumerate(broadcast_data)])
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
                data_to_return = [self._known_types[each_val[1]](each_val[0]) for each_val in data["data"].values()]
                print(f"Data to return : {data_to_return}")
                if len(data_to_return) == 1:
                    # Fix weird ack issue
                    data_to_return = data_to_return[0]
                return data_to_return



class BroadcastHost(Broadcast):

    def __init__(self, topics):
        connection, additional_data = setup_server_connection(ip=constants.BROADCAST_IP,
                                                              port=constants.BROADCAST_PORT,
                                                              num_connections=1)

        super().__init__(topics = topics,
                         connection = connection,
                         additional_data = additional_data)


class BroadcastClient(Broadcast):

    def __init__(self, topics):
        connection, additional_data = setup_client_connection(ip=constants.BROADCAST_IP,
                                                              port = constants.BROADCAST_PORT)

        super().__init__(topics = topics,
                         connection = connection,
                         additional_data = additional_data)







def wait(time_to_wait : int):
    time.sleep(time_to_wait / 1000)


class ColorHSV:

    def __init__(self,
                 h,
                 s,
                 v):
        self._h = h
        self._s = s
        self._v = v

    def __eq__(self, other):
        return self._h == other._h and self._s == other._s and self._v == other._v

class Color:

    RED = ColorHSV(h=0,
                   s=100,
                   v=100)

    ORANGE = ColorHSV(h=30,
                      s=100,
                      v=100)
    YELLOW = ColorHSV(h=60,
                      s=100,
                      v=100)

    GREEN = ColorHSV(h=120,
                     s=100,
                     v=100)

    CYAN = ColorHSV(h=180,
                    s=100,
                    v=100)

    BLUE = ColorHSV(h=240,
                    s = 100,
                    v = 100)

    VIOLET = ColorHSV(h=270,
                      s=100,
                      v=100)

    MAGENTA = ColorHSV(h=300,
                       s=100,
                       v=100)

    WHITE = ColorHSV(h=0,
                     s=0,
                     v=100)

    GRAY = ColorHSV(h=0,
                    s=0,
                    v=50)

    BLACK = ColorHSV(h=0,
                     s=0,
                     v=10)

    NONE = ColorHSV(h=0,
                    s=0,
                    v=0)



