try:
    from pybricks.tools import wait
except ImportError:
    import sys
    import os
    sys.path.append(os.path.abspath("../.."))
    from mock_pybricks import wait
    from distance_test_cases import DISTANCE_TESTS
    
   
from rover_spike_hub import RoverSpikeHub
import constants

def main():
    test_id = "BACKWARDS_100_CM"

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
    print("Test Complete!")

def run_test_case(test_id, rover):
    parameters = DISTANCE_TESTS[test_id]

    if parameters["movement_type"] == "straight":
        print(f"Driving straight with a distance of {parameters['distance']}")
        rover.drive(angle=0, distance=parameters["distance"])

    elif parameters["movement_type"] == "curve":
        print(f"Driving at a curve with a distance of {parameters['distance']} and angle {parameters['angle']}")
        rover.drive(angle=parameters["angle"], distance=parameters['distance'])

if __name__ == "__main__":
    main()