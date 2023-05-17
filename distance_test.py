print("r u running")
import umath as math
from pybricks.parameters import Direction
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase
from pybricks.tools import wait

import constants
from utils import PoweredUpHub


HUB = PoweredUpHub()

L_MOTOR = Motor(port=HUB.get_port_from_str(constants.LEFT_MOTOR_PORT),
                        positive_direction=Direction.CLOCKWISE)

R_MOTOR = Motor(port=HUB.get_port_from_str(constants.RIGHT_MOTOR_PORT),
                        positive_direction=Direction.COUNTERCLOCKWISE)

STEERING_MOTOR = Motor(port=HUB.get_port_from_str(constants.STEERING_MOTOR_PORT),
                               positive_direction=Direction.COUNTERCLOCKWISE)

DRIVE_BASE = DriveBase(left_motor=L_MOTOR, right_motor=R_MOTOR, wheel_diameter=constants.WHEEL_DIAMETER,
                        axle_track=constants.AXLE_TRACK)



def move_forward(distance):
    pass

    
def main():
    print("Driving forward 1m")
    rover.move_forward(rover, 1000)
    print("Goodnight!")

main()

print("hello")