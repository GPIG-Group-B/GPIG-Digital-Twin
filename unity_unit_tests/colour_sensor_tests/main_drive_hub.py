try:
    import sys
    import os
    sys.path.append(os.path.abspath("../.."))
except ImportError:
    pass

from rover_drive_hub import RoverPoweredUpHub
import constants



def main():

    rover = RoverPoweredUpHub(wheel_diam=constants.WHEEL_DIAMETER,
                  axle_track=constants.AXLE_TRACK,
                  max_turn_angle=constants.MAX_TURN_ANGLE,
                  wheelbase=constants.WHEELBASE,
                  height=constants.ROVER_HEIGHT,
                  width=constants.ROVER_WIDTH,
                  depth=constants.ROVER_DEPTH)

    print("Let's-a go!")
    rover.run()
    rover.shutdown()
    print("Goodnight!")


if __name__ == "__main__":
    main()