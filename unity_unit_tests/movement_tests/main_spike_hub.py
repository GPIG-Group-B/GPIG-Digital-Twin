try:
    from pybricks.tools import wait
except ImportError:
    import sys
    import os
    sys.path.append(os.path.abspath("../.."))
    from mock_pybricks import wait
    
   
from rover_spike_hub import RoverSpikeHub
import constants
import json

with open('../../distance_test_cases.json') as json_file:
    TEST_CASES = json.load(json_file)

def main():
    # print("----------------------")

    # rover = RoverSpikeHub(wheel_diam=constants.WHEEL_DIAMETER,
    #               axle_track=constants.AXLE_TRACK,
    #               max_turn_angle=constants.MAX_TURN_ANGLE,
    #               wheelbase=constants.WHEELBASE,
    #               height=constants.ROVER_HEIGHT,
    #               width=constants.ROVER_WIDTH,
    #               depth=constants.ROVER_DEPTH)

    # print("Let's drive!")
    # rover.drive(angle=0,
    #             distance=1000)
    # print("Completed first drive")
    # wait(2000)

    # rover.drive(angle=0,
    #         distance=-1000)
    # print("Completed second drive")
    # wait(2000)

    # print("Shutting down")
    # rover.shutdown()
    # print("All done!")
    print(TEST_CASES)




if __name__ == "__main__":
    main()