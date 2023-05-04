from connection_utils import setup_server_connction, send_json_message, send_device_type_id, receive_json
import socket

class Direction:

    COUNTERCLOCKWISE = "COUNTERCLOCKWISE"
    CLOCKWISE = "clockwise"

class PybricksDevice:

    def __init__(self, port, device_type_id):
        self._port, self._additional_data = setup_server_connction(ip=port.ip,
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


