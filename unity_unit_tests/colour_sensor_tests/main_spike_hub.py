try:
    from pybricks.tools import wait
except ImportError:
    import sys
    import os
    sys.path.append(os.path.abspath("../.."))
    from mock_pybricks import wait
    from mock_pybricks import Color
    from colour_test_cases import COLOUR_TESTS
   
from rover_spike_hub import RoverSpikeHub
import constants

colour_mapping_dict = {"blue": Color.BLUE,"yellow": Color.YELLOW, "white": Color.WHITE, "grey": Color.GRAY}

def main():
    test_id = "CD_GREY"

    print("----------------------")
    print(f"Starting test with ID = {test_id}.")
    print("----------------------")

    rover = RoverSpikeHub(wheel_diam=constants.WHEEL_DIAMETER,
                  axle_track=constants.AXLE_TRACK,
                  max_turn_angle=constants.MAX_TURN_ANGLE,
                  wheelbase=constants.WHEELBASE,
                  height=constants.ROVER_HEIGHT,
                  width=constants.ROVER_WIDTH,
                  depth=constants.ROVER_DEPTH)
    
    run_test_case(test_id, rover)

    print("Shutting down")
    rover.shutdown()
    print("Test Complete")

def run_test_case(test_id, rover):
    parameters = COLOUR_TESTS[test_id]

    print(f"Checking colour of sensor {parameters['sensor']}:")
    if parameters["sensor"] == "front":
        colour = rover.detect_colour_primary()
    else:
        colour = rover.detect_colour_secondary()
    
    print(f"Colour detected - HSV({colour._h, colour._s, colour._v})")
    print(f"Matches Color.{parameters['colour'].upper()} - {colour_mapping_dict[parameters['colour']] == colour}")

if __name__ == "__main__":
    main()