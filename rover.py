import umath as math
from pybricks.parameters import Direction
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase

from sensors import UltrasonicScanner
from utils import convert_str_to_port


class Rover:
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
        ultrasonic_scanner (UltrasonicScanner) :
            The ultrasonic scanner used to scan the surroundings
    """

    def __init__(self,
                 wheel_diam: int,
                 axle_track: int,
                 left_motor_port: str,
                 right_motor_port: str,
                 steering_motor_port: str,
                 ultrasonic_scanner: UltrasonicScanner,
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
        self._left_motor, self._right_motor, self._steering_motor = self._setup_motors(left_motor_port=left_motor_port,
                                                                                       right_motor_port=right_motor_port,
                                                                                       steering_motor_port=steering_motor_port)

        self._drive_base = DriveBase(left_motor=self._left_motor,
                                     right_motor=self._right_motor,
                                     wheel_diameter=self._wheel_diam,
                                     axle_track=self._axle_track)
        self.ultrasonic_scanner = ultrasonic_scanner

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

    def _setup_motors(self,
                      left_motor_port: str,
                      right_motor_port: str,
                      steering_motor_port: str):
        """Utility method to setup motors when Rover __init__ func is called

        Args:
            left_motor_port:
                Port letter assignment for left motor
            right_motor_port:
                Port letter assignment for right motor
            steering_motor_port:
                Steering letter assignment for steering motor

        Returns:
            three Motor objects corresponding to the left motor, right motor and steering motor respectively
        """
        l_motor = Motor(port=convert_str_to_port(left_motor_port),
                                 positive_direction=Direction.CLOCKWISE)
        r_motor = Motor(port=convert_str_to_port(right_motor_port),
                                  positive_direction=Direction.COUNTERCLOCKWISE)
        steering_motor = Motor(port=convert_str_to_port(steering_motor_port),
                                     positive_direction=Direction.COUNTERCLOCKWISE)
        return l_motor, r_motor, steering_motor



    def drive(self,
              angle: int,
              distance : int):
        """ Utility function to drive rover in a certain direction for a set distance

        Args:
            angle:
                Angle to drive at in degrees
            distance:
                Distance to drive in mm

        Returns:
            None
        """
        if abs(angle) > self._max_turn_angle:
            raise ValueError(f"Provided angle {angle} must be less than the max turn angle : {self._max_turn_angle}")
        DEFAULT_SPEED = 100

        self._steering_motor.run_target(speed=DEFAULT_SPEED,
                                        target_angle=angle)
        if angle == 0:
            self._drive_base.straight(distance=distance)
        else:
            rad = self._wheelbase / math.tan(math.radians(angle)) + self._axle_track / 2
            arc = 360 * (distance / (2 * math.pi * rad))
            self._drive_base.curve(radius=rad,
                                   angle=arc)

    def scan_surroundings(self):
        """Utility function for scanning surrounds using ultrasonic sensor using default scan range

        Returns:
            list[Tuple(angle, distance))] : List of angles and distance tuples
        """
        return self.ultrasonic_scanner.sweep()
