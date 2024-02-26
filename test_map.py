from map import Map
from rover_spike_hub import RoverSpikeHub
import constants
try:
    from pybricks.tools import wait
except ImportError:
    from mock_pybricks import wait


def run_test(start_x,start_y,start_angle,target_x,target_y,target_angle,resolution=0.25):
    """
    Parameters:
        start_x (float): starting pos x in m
        start_y (float): starting pos y in m
        start_angle (int): starting heading relative to map north +y
        target_x (float): end goal x in m
        target_y (float): end goal y in m
        target_angle (int): end heading relative to map north +y
        (optinal) resolution (float): resolution of path finding in m
    """
    sx = int(start_x/resolution+0.5)
    sy = int(start_y/resolution+0.5)
    gx = int(target_x/resolution+0.5)
    gy = int(target_y/resolution+0.5)
    test = Map(size_x=3.5, size_y=3, resolution=resolution, starting_position_x=sx, starting_position_y=sy, goal_node_x=gx, goal_node_y=gy)

    ## BOX AT ~ 0.75m 1.5m
    test.add_obstacle(x=2, y=4)
    test.add_obstacle(x=3, y=4)
    test.add_obstacle(x=2, y=5)
    test.add_obstacle(x=3, y=5)

    ## Box AT ~ 2.25m 1.5m
    test.add_obstacle(x=8, y=4)
    test.add_obstacle(x=9, y=4)
    test.add_obstacle(x=8, y=5)
    test.add_obstacle(x=9, y=5)

    ## BIG HOLE NO TOUCHY
    test.add_obstacle(x=2, y=8)
    test.add_obstacle(x=2, y=9)
    test.add_obstacle(x=2, y=10)
    test.add_obstacle(x=2, y=11)
    test.add_obstacle(x=3, y=8)
    test.add_obstacle(x=3, y=9)
    test.add_obstacle(x=3, y=10)
    test.add_obstacle(x=3, y=11)
    test.add_obstacle(x=4, y=8)
    test.add_obstacle(x=4, y=9)
    test.add_obstacle(x=4, y=10)
    test.add_obstacle(x=4, y=11)
    test.add_obstacle(x=5, y=8)
    test.add_obstacle(x=5, y=9)
    test.add_obstacle(x=5, y=10)
    test.add_obstacle(x=5, y=11)
    test.add_obstacle(x=6, y=8)
    test.add_obstacle(x=6, y=9)
    test.add_obstacle(x=6, y=10)
    test.add_obstacle(x=6, y=11)
    test.add_obstacle(x=7, y=8)
    test.add_obstacle(x=7, y=9)
    test.add_obstacle(x=7, y=10)
    test.add_obstacle(x=7, y=11)




    test.set_start_heading(start_angle)
    test.set_target_heading(target_angle)
    return test
    # goal_node, start_node, all_nodes = test.convert_to_graph()

    # test_d_star = DStarLite(start_node=start_node,
    #                 goal_node=goal_node,
    #                 all_nodes=all_nodes,
    #                 cost_func=test.cost,
    #                 move_func=test.update_current_position_by_node)
    #
    # visualiser = MapVisualiser(map = test, pathfinding_alg=test_d_star)


rover = RoverSpikeHub(wheel_diam=constants.WHEEL_DIAMETER,
              axle_track=constants.AXLE_TRACK,
              max_turn_angle=constants.MAX_TURN_ANGLE,
              wheelbase=constants.WHEELBASE,
              height=constants.ROVER_HEIGHT,
              width=constants.ROVER_WIDTH,
              depth=constants.ROVER_DEPTH)

demo_map = run_test(0.75,0.25,0,3.0,0.75,90,resolution=0.25)
rover.load_map(demo_map)

rover.navigate_map(cost_func=demo_map.cost)
rover.shutdown()
##run_test(3.25,0.75,90,2.75,2.75,0,resolution=0.25)