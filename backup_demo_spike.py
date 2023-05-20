from rover_spike_hub import RoverSpikeHub
import constants
try:
    from pybricks.tools import wait
except ImportError:
    from time import sleep as wait
    import sys
    import os


def main():
    print("----------------------")

    rover = RoverSpikeHub(wheel_diam=constants.WHEEL_DIAMETER,
                  axle_track=constants.AXLE_TRACK,
                  max_turn_angle=constants.MAX_TURN_ANGLE,
                  wheelbase=constants.WHEELBASE,
                  height=constants.ROVER_HEIGHT,
                  width=constants.ROVER_WIDTH,
                  depth=constants.ROVER_DEPTH)

    rover.drive(angle=0,
                distance=100)
    # rover.drive_tar




if __name__ == "__main__":
    main()