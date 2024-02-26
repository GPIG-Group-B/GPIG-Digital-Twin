from map import Map
from rover_spike_hub import RoverSpikeHub
import constants
try:
    from pybricks.tools import wait
except ImportError:
    from mock_pybricks import wait


def main():
    print("----------------------")

    rover = RoverSpikeHub(wheel_diam=constants.WHEEL_DIAMETER,
                  axle_track=constants.AXLE_TRACK,
                  max_turn_angle=constants.MAX_TURN_ANGLE,
                  wheelbase=constants.WHEELBASE,
                  height=constants.ROVER_HEIGHT,
                  width=constants.ROVER_WIDTH,
                  depth=constants.ROVER_DEPTH)

    print("Let's drive!")
    rover.drive(angle=0,
                distance=100)
    print("Completed first drive")
    
    rover.drive(angle=0,
            distance=-100)
    print("Completed second drive")

    # map = Map(size_x=1,
    #            size_y=1,
    #            resolution=0.25,
    #            starting_position_x=0,
    #            starting_position_y=0,
    #            goal_node_x=2,
    #            goal_node_y=2)
    # rover.load_map(map)

    # rover.navigate_map(cost_func=map.cost)

    print("Shutting down")
    rover.shutdown()
    print("All done!")




if __name__ == "__main__":
    main()