try:
    from pybricks.tools import wait
except ImportError:
    import sys
    import os
    sys.path.append(os.path.abspath("../.."))
    from mock_pybricks import wait
    from mock_pybricks import Color
    import json

with open('../../colour_test_cases.json') as json_file:
    TEST_CASES = json.load(json_file)
   
from rover_spike_hub import RoverSpikeHub
import constants

colour_mapping_dict = {"blue": Color.BLUE}

def main(test_id):
    print("----------------------")
    print("Beginning colour sensor test")
    print("----------------------")

    rover = RoverSpikeHub(wheel_diam=constants.WHEEL_DIAMETER,
                  axle_track=constants.AXLE_TRACK,
                  max_turn_angle=constants.MAX_TURN_ANGLE,
                  wheelbase=constants.WHEELBASE,
                  height=constants.ROVER_HEIGHT,
                  width=constants.ROVER_WIDTH,
                  depth=constants.ROVER_DEPTH)
    
    parameters = TEST_CASES[test_id]

    print(f"Checking colour of sensor {parameters['sensor']}:")
    if parameters["sensor"] == "front":
        colour = rover.detect_colour_primary()
    else:
        colour = rover.detect_colour_secondary()
    
    print(f"Colour detected - {colour} = {colour._h, colour._s, colour._v}")
    print(f"Matches test case - {parameters['colour'] == colour}")

    print("Shutting down")
    rover.shutdown()
    print("All done!")


if __name__ == "__main__":
    main("CD_BLUE")