try:
    import umath as math
    from pybricks.parameters import Direction
    from pybricks.pupdevices import Motor
    from pybricks.robotics import DriveBase
    from pybricks.experimental import Broadcast
    from pybricks.tools import wait
    from pybricks.hubs import TechnicHub
    from pybricks.parameters import Color
except ImportError:
    import math
    from mock_pybricks import Motor, DriveBase,ColorSensor, ForceSensor, ColorDistanceSensor, Direction, wait
    from mock_pybricks import BroadcastClient as Broadcast

import constants
from sensors import UltrasonicScanner
from utils import LegoSpikeHub, PoweredUpHub
from radio import Radio


class RoverPoweredUpHub:
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
        self._powered_up_hub = PoweredUpHub()
        self._radio = Radio(topics=["drive", "shutdown", "complete"],
                            broadcast_func=Broadcast)

        self._left_motor, self._right_motor, self._steering_motor = self._setup_motors()

        self._drive_base = DriveBase(left_motor=self._left_motor,
                                     right_motor=self._right_motor,
                                     wheel_diameter=self._wheel_diam,
                                     axle_track=self._axle_track)
        try:
            hub = TechnicHub()
            hub.light.on(Color.RED)
        except:
            pass

    def shutdown(self):
        try:
            self._left_motor.send_shutdown_message()
            self._right_motor.send_shutdown_message()
            self._steering_motor.send_shutdown_message()
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

    def _setup_motors(self):
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
        l_motor = Motor(port=self._powered_up_hub.get_port_from_str(constants.LEFT_MOTOR_PORT),
                        positive_direction=Direction.CLOCKWISE)
        r_motor = Motor(port=self._powered_up_hub.get_port_from_str(constants.RIGHT_MOTOR_PORT),
                        positive_direction=Direction.COUNTERCLOCKWISE)
        steering_motor = Motor(port=self._powered_up_hub.get_port_from_str(constants.STEERING_MOTOR_PORT),
                               positive_direction=Direction.COUNTERCLOCKWISE)
        return l_motor, r_motor, steering_motor

    def run(self):
        while True:
            data = self._radio.receive("drive")
            if data:
                angle, distance, command_id = data
                successful = self.drive(angle, distance)
                if successful:
                    print(f"Sending completion confirmation with command id {command_id}")
                    self._radio.send("complete", (command_id,))
            wait(50)
            should_shutdown = self._radio.receive("shutdown")
            if should_shutdown is not None:
                print("Shutting down")
                wait(1000) # Wait enough time for the other hub to get the acknowledgement
                return

    def drive_target(self, desired_angle, distance):

        x = math.degrees(math.atan(self._wheelbase/((distance/math.radians(desired_angle))-(self._axle_track/2))))
        self.drive(angle=x,
                distance=distance)

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
        if abs(angle) > self._max_turn_angle:
            raise ValueError(f"Provided angle {angle} must be less than the max turn angle : {self._max_turn_angle}")
        DEFAULT_SPEED = 100

        self._steering_motor.run_target(speed=DEFAULT_SPEED,
                                        target_angle=angle)
        if angle == 0:
            self._drive_base.straight(distance=distance, wait=False)
        else:
            rad = self._wheelbase / math.tan(math.radians(angle)) + self._axle_track / 2
            arc = 360 * (distance / (2 * math.pi * rad))
            self._drive_base.curve(radius=rad,
                                   angle=arc, 
                                   wait=False)

        while True:
            drive_done = self._drive_base.done()
            # print(f"drive base is done = {self._drive_base.done()}")
            if drive_done:
                return True
            stop = self._radio.receive("drive")
            if stop:
                print("Emergency stop:", stop)
                if stop[1] == 0:
                    self._drive_base.stop()
                    print("EMERGENCY STOP!")
                    return False
            wait(10)
    
        # Now that we're done driving, we can return, and the run() function will send the complete message to the main hub