import umath as math
from pybricks.parameters import Direction
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import wait
import json

import constants
from utils import PoweredUpHub

with open('distance_test_cases.json') as json_file:
    TEST_CASES = json.load(json_file)

# Initalises motors needed to test driving
HUB = PoweredUpHub()
L_MOTOR = Motor(port=HUB.get_port_from_str(constants.LEFT_MOTOR_PORT),
                positive_direction=Direction.COUNTERCLOCKWISE)
R_MOTOR = Motor(port=HUB.get_port_from_str(constants.RIGHT_MOTOR_PORT),
                positive_direction=Direction.CLOCKWISE)
STEERING_MOTOR = Motor(port=HUB.get_port_from_str(constants.STEERING_MOTOR_PORT),
                       positive_direction=Direction.COUNTERCLOCKWISE, gears=[12, 36])
DRIVE_BASE = DriveBase(left_motor=L_MOTOR, right_motor=R_MOTOR, wheel_diameter=constants.WHEEL_DIAMETER,
                       axle_track=constants.AXLE_TRACK)


def move_straight(distance):
    """Moves the rover in a straight line for a given distance."""
    print(f"Moving straight for distance {distance}.")
    # DRIVE_BASE.straight(distance, wait=True)


def drive_at_curve(angle, distance):
    """Moves the rover at an angle for a specified distance."""
    print(f"Driving at a curve with angle {angle} and distance {distance}.")

    if abs(angle) > constants.MAX_TURN_ANGLE:
        raise ValueError(
            f"Provided angle {angle} must be less than the max turn angle : {constants.MAX_TURN_ANGLE}")

    DEFAULT_SPEED = 100

    STEERING_MOTOR.run_target(speed=DEFAULT_SPEED, target_angle=angle)

    if angle == 0:
        raise ValueError("Angle of 0 is not a curve")
    else:
        rad = constants.WHEELBASE / \
            math.tan(math.radians(angle)) + constants.AXLE_TRACK / 2
        arc = 360 * (distance / (2 * math.pi * rad))
        DRIVE_BASE.curve(radius=rad, angle=arc)


def run_test_case(test_id):
    parameters = TEST_CASES[test_id]
    if parameters["movement_type"] == "straight":
        move_straight(parameters["distance"])
    elif parameters["movement_type"] == "curve":
        drive_at_curve(parameters["angle"], parameters["distance"])


def main():
    test_id = "BACKWARDS_100_CM"

    print("----------------------")
    print(f"Starting test with ID = {test_id}.")
    print("----------------------")

    run_test_case(test_id)
    print("Test Complete")


main()
