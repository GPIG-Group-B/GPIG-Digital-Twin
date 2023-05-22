try:
    from pybricks.tools import wait
except ImportError:
    import sys
    import os
    sys.path.append(os.path.abspath("../.."))
    from mock_pybricks import wait
   
from rover_spike_hub import RoverSpikeHub
import constants

def main():
    print("----------------------")

    rover = RoverSpikeHub(wheel_diam=constants.WHEEL_DIAMETER,
                  axle_track=constants.AXLE_TRACK,
                  max_turn_angle=constants.MAX_TURN_ANGLE,
                  wheelbase=constants.WHEELBASE,
                  height=constants.ROVER_HEIGHT,
                  width=constants.ROVER_WIDTH,
                  depth=constants.ROVER_DEPTH)

    print("Let's-a go!")
    wait(2000)
    rover.shutdown()
    print("Goodnight!")




if __name__ == "__main__":
    main()