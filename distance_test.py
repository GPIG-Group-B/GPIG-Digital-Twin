import umath as math
from pybricks.parameters import Direction
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import wait

import constants
from utils import PoweredUpHub


HUB = PoweredUpHub()

L_MOTOR = Motor(port=HUB.get_port_from_str(constants.LEFT_MOTOR_PORT),
                        positive_direction=Direction.COUNTERCLOCKWISE)

R_MOTOR = Motor(port=HUB.get_port_from_str(constants.RIGHT_MOTOR_PORT),
                        positive_direction=Direction.CLOCKWISE)

STEERING_MOTOR = Motor(port=HUB.get_port_from_str(constants.STEERING_MOTOR_PORT),
                               positive_direction=Direction.COUNTERCLOCKWISE)

DRIVE_BASE = DriveBase(left_motor=L_MOTOR, right_motor=R_MOTOR, wheel_diameter=constants.WHEEL_DIAMETER,
                        axle_track=constants.AXLE_TRACK)

def move_straight(distance, forward=True):
    if forward:
        DRIVE_BASE.straight(distance, wait=True)
    else:
        DRIVE_BASE.straight(-distance, wait=True)

def drive_at_curve(angle, distance):
    if abs(angle) > constants.MAX_TURN_ANGLE:
        raise ValueError(f"Provided angle {angle} must be less than the max turn angle : {constants.MAX_TURN_ANGLE}")

    DEFAULT_SPEED = 100

    STEERING_MOTOR.run_target(speed=DEFAULT_SPEED, target_angle=angle)

    if angle == 0:
        raise ValueError("Angle of 0 is not a curve")
    else:
        rad = constants.WHEELBASE / math.tan(math.radians(angle)) + constants.AXLE_TRACK / 2
        arc = 360 * (distance / (2 * math.pi * rad))
        DRIVE_BASE.curve(radius=rad, angle=arc)

def main():
    # Forward Tests
    move_straight(1000) # 1m
    move_straight(500) # 50cm
    move_straight(250) # 25cm
    move_straight(200) # 20cm
    move_straight(100) # 10cm

    # Backwards Tests
    move_straight(1000, forward=False) # 1m
    move_straight(500, forward=False) # 50cm
    move_straight(250, forward=False) # 25cm
    move_straight(200, forward=False) # 20cm
    move_straight(100, forward=False) # 10cm

    # Curve Tests
    ## 5 degrees left forward
    drive_at_curve(-5, 500) # 50cm
    drive_at_curve(-5, 250) # 25cm
    drive_at_curve(-5, 100) # 10cm

    # 5 degrees right forward
    drive_at_curve(5, 500) # 50cm
    drive_at_curve(5, 250) # 25cm
    drive_at_curve(5, 100) # 10cm

    ## 5 degrees left backwards
    drive_at_curve(-5, -500) # 50cm
    drive_at_curve(-5, -250) # 25cm
    drive_at_curve(-5, -100) # 10cm

    # 5 degrees right backwards
    drive_at_curve(5, -500) # 50cm
    drive_at_curve(5, -250) # 25cm
    drive_at_curve(5, -100) # 10cm

    # ----------------------------

    ## 10 degrees left forward
    drive_at_curve(-10, 500) # 50cm
    drive_at_curve(-10, 250) # 25cm
    drive_at_curve(-10, 100) # 10cm

    # 10 degrees right forward
    drive_at_curve(10, 500) # 50cm
    drive_at_curve(10, 250) # 25cm
    drive_at_curve(10, 100) # 10cm

    ## 10 degrees left backwards
    drive_at_curve(-10, -500) # 50cm
    drive_at_curve(-10, -250) # 25cm
    drive_at_curve(-10, -100) # 10cm

    # 10 degrees right backwards
    drive_at_curve(10, -500) # 50cm
    drive_at_curve(10, -250) # 25cm
    drive_at_curve(10, -100) # 10cm

    # ----------------------------
    ## 15 degrees left forward
    drive_at_curve(-15, 500) # 50cm
    drive_at_curve(-15, 250) # 25cm
    drive_at_curve(-15, 100) # 10cm

    # 15 degrees right forward
    drive_at_curve(15, 500) # 50cm
    drive_at_curve(15, 250) # 25cm
    drive_at_curve(15, 100) # 10cm

    ## 15 degrees left backwards
    drive_at_curve(-15, -500) # 50cm
    drive_at_curve(-15, -250) # 25cm
    drive_at_curve(-15, -100) # 10cm

    # 15 degrees right backwards
    drive_at_curve(15, -500) # 50cm
    drive_at_curve(15, -250) # 25cm
    drive_at_curve(15, -100) # 10cm

main()

print("hello")