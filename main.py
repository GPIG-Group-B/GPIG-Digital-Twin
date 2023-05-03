from rover import Rover
import constants
from sensors import UltrasonicScanner


def main():

    rover = Rover(wheel_diam=constants.WHEEL_DIAMETER,
                  axle_track=constants.AXLE_TRACK,
                  max_turn_angle=constants.MAX_TURN_ANGLE,
                  wheelbase=constants.WHEELBASE,
                  height=constants.ROVER_HEIGHT,
                  width=constants.ROVER_WIDTH,
                  depth=constants.ROVER_DEPTH)

    rover.drive(angle=0,
                distance=100)
    # rover.scan_surroundings()
    rover.shutdown()




if __name__ == "__main__":
    main()