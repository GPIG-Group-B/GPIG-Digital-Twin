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

def main(test_id):
    print("----------------------")
    print("Beginning movement test")
    print("----------------------")

    rover = RoverSpikeHub(wheel_diam=constants.WHEEL_DIAMETER,
                  axle_track=constants.AXLE_TRACK,
                  max_turn_angle=constants.MAX_TURN_ANGLE,
                  wheelbase=constants.WHEELBASE,
                  height=constants.ROVER_HEIGHT,
                  width=constants.ROVER_WIDTH,
                  depth=constants.ROVER_DEPTH)

    parameters = TEST_CASES[test_id]

    if parameters["movement_type"] == "straight":
        print(f"Driving straight with a distance of {parameters['distance']}")
        rover.drive(angle=0, distance=parameters["distance"])

    elif parameters["movement_type"] == "curve":
        print(f"Driving at a curve with a distance of {parameters['distance']} and angle {parameters['angle']}")
        rover.drive(angle=parameters["angle"], distance=parameters['distance'])

    print("Shutting down")
    rover.shutdown()
    print("All done!")

if __name__ == "__main__":
    main("BACKWARDS_100_CM")