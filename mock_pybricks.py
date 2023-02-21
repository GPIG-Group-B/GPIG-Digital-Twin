from connection_utils import setup_server_connction, send_json_message, send_device_type_id


class Port:
    A = {"ip" : "localhost", "port" : 65432}
    B = {"ip" : "localhost", "port" : 65433}
    C = {"ip" : "localhost", "port" : 65434}
    D = {"ip" : "localhost", "port" : 65435}
    E = {"ip" : "localhost", "port" : 65436}
    F = {"ip" : "localhost", "port" : 65437}

class Direction:

    COUNTER_CLOCKWISE = "counter_clockwise"
    CLOCKWISE = "clockwise"


class Motor:

    def __init__(self,
                 port : dict,
                 positive_direction : Direction,
                 gears : list,
                 reset_angle : bool):
        self._DEVICE_TYPE_ID = 0
        self._port, self._additional_data = setup_server_connction(**port,
                                                                   num_connections=1)
        send_device_type_id(connection=self._port, device_type_id=self._DEVICE_TYPE_ID)
        self._positive_direction = positive_direction
        self._gears = gears
        self._reset_angle = reset_angle
        self._speed = 0
        self._angle = 0
        self._load = "unknown"
        self._send_info_message()


    def _send_info_message(self):
        EXCLUDE_FROM_INFO_MESSAGE = ["port", "additional_data"]
        send_json_message(connection=self._port,
                          message_dict={key.strip("_") : val for key,val in vars(self).items() if not any(exclusion in key for exclusion in EXCLUDE_FROM_INFO_MESSAGE)},
                          message_id=self._DEVICE_TYPE_ID)


    def speed(self):
        return self._speed

    def angle(self):
        return self._angle

    def reset_angle(self, angle : int):
        self._angle = angle

    def stop(self):
        MESSAGE_ID = 0
        send_json_message(connection=self._port,
                          message_dict={},
                          message_id=MESSAGE_ID)

    def brake(self):
        MESSAGE_ID = 1
        send_json_message(connection=self._port,
                          message_dict={},
                          message_id=MESSAGE_ID)
    def hold(self):
        MESSAGE_ID = 2
        send_json_message(connection=self._port,
                          message_dict={},
                          message_id=MESSAGE_ID)

    def run(self, speed : int):
        MESSAGE_ID = 4
        send_json_message(connection=self._port,
                          message_dict={"speed" : speed},
                          message_id=MESSAGE_ID)

    def run_time(self, speed : int, time : int, then = None, wait = True):
        MESSAGE_ID = 5
        send_json_message(connection=self._port,
                          message_dict={"speed" : speed,
                                        "time" : time,
                                        "then" : then,
                                        "wait" : wait},
                          message_id=MESSAGE_ID)

    def run_angle(self, speed : int, rotation_angle : int, then = None, wait=True):
        MESSAGE_ID = 6
        send_json_message(connection=self._port,
                          message_dict={"speed": speed,
                                        "rotation_angle": rotation_angle,
                                        "then": then,
                                        "wait": wait},
                          message_id=MESSAGE_ID)




