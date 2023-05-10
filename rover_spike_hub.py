try:
    from pybricks.parameters import Direction
    from pybricks.pupdevices import Motor, ColorSensor, ForceSensor, ColorDistanceSensor
    from pybricks.robotics import DriveBase
    from pybricks.experimental import Broadcast

except ImportError:
    from mock_pybricks import Motor, DriveBase,ColorSensor, ForceSensor, ColorDistanceSensor, Direction
    from mock_pybricks import BroadcastHost as Broadcast

import constants
from sensors import UltrasonicScanner
from utils import LegoSpikeHub
from radio import Radio


class RoverSpikeHub:
    """Rover class for controlling the lego spike rover

    Attributes:
        _height (int) :
            The height of the rover in mm
        _width (int) :
            The width of the rover in mm
        _depth (int) :
            The width of the rover in mm
        _axle_track (int):
            Distance between points where driving wheels touch the ground in mm
        _wheel_diam (int):
            Diameter of wheels in mm
        _max_turn_angle (int):
            Max angle the rover can turn in degrees
        _wheelbase (int) :
            The wheelbase of the rover in mm
        _left_motor (Motor) :
            pybricks Motor object for the left motor
        _right_motor (Motor) :
            pybricks Motor object for the right motor
        _drive_base (DriveBase) :
            DriveBase object used to make it easier to drive the rover using the two driving motors
        _ultrasonic_scanner (UltrasonicScanner) :
            The ultrasonic scanner used to scan the surroundings
    """

    def __init__(self,
                 wheel_diam: int,
                 axle_track: int,
                 height: int = None,
                 width: int = None,
                 depth: int = None,
                 max_turn_angle: int = 22,
                 wheelbase: int = 120):
        """ Init method for Mars Rover class

        Args:
            wheel_diam:
                Diameter of wheels in mm
            axle_track:
                Distance between points where driving wheels touch the ground in mm
            left_motor_port:
                Port letter assignment for left motor
            right_motor_port:
                Port letter assignment for right motor
            steering_motor_port:
                Port letter assignment for steering motor
            ultrasonic_scanner:
                Rovers ultrasonic scanner used for mapping the surrounding area
            height:
                Height of rover in mm
            width:
                Width of rover in mm
            depth:
                Depth of rover in mm
            max_turn_angle:
                Max angle the rover can turn in degrees
            wheelbase:
                Wheelbase of the rover in mm
        """
        self._height, self._width, self._depth = height, width, depth
        self._axle_track = axle_track
        self._wheel_diam = wheel_diam
        self._max_turn_angle = max_turn_angle
        self._wheelbase = wheelbase
        self._lego_spike_hub = LegoSpikeHub()

        self._force_sensor = ForceSensor(port=self._lego_spike_hub.get_port_from_str(constants.FORCE_SENSOR_PORT))
        self._colour_distance_sensor = ColorDistanceSensor(port=self._lego_spike_hub.get_port_from_str(constants.COLOUR_DISTANCE_SENSOR_PORT))
        self._ultrasonic_scanner = UltrasonicScanner(motor_port=self._lego_spike_hub.get_port_from_str(constants.ULTRASONIC_MOTOR_PORT),
                                                     sensor_port=self._lego_spike_hub.get_port_from_str(constants.ULTRASONIC_SENSOR_PORT),
                                                     default_scan_start_deg=constants.SCAN_START,
                                                     default_scan_end_deg=constants.SCAN_END,
                                                     gear_ratio=constants.GEAR_RATIO)
        self._colour_sensor = ColorSensor(port = self._lego_spike_hub.get_port_from_str(constants.COLOUR_SENSOR_PORT))

        self._radio = Radio(topics=["drive", "shutdown"],
                            broadcast_func=Broadcast)



    def shutdown(self):
        self._radio.send("shutdown", (1,))
        try:
            self._ultrasonic_scanner.send_shutdown_message()
            self._colour_sensor.send_shutdown_message()
            self._force_sensor.send_shutdown_message()
            self._colour_distance_sensor.send_shutdown_message()
            self._radio.shutdown()
        except:
            pass

    def set_max_turn_angle(self,
                           new_max_angle: int):
        """Setter to update max turn angle

        Args:
            new_max_angle:
                New maximum turning angle in mm

        Returns:
            None

        """
        self._max_turn_angle = new_max_angle



    def drive(self,
              angle: int,
              distance: int):
        """ Utility function to drive rover in a certain direction for a set distance

        Args:
            angle:
                Angle to drive at in degrees
            distance:
                Distance to drive in mm

        Returns:
            None
        """
        self._radio.send("drive",
                         (angle, distance))

    def scan_surroundings(self):
        """Utility function for scanning surrounds using ultrasonic sensor using default scan range

        Returns:
            list[Tuple(angle, distance))] : List of angles and distance tuples
        """
        return self._ultrasonic_scanner.sweep()
