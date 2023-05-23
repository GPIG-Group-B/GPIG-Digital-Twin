import math

from map import Map, EmptyTile, RoverTile, ObstacleTile, GoalTile, MapVisualiser
from d_star_lite import DStarLite

# def cost_func(x,y):
    # if not isinstance(x, (EmptyTile,GoalTile, RoverTile)) or not isinstance(y, (EmptyTile,GoalTile)):
    #     return float("inf")
    # else:
    # return math.dist([x.pos_x, x.pos_y], [y.pos_x, y.pos_y])


test = Map(size_x=3, size_y=3.6, resolution=0.2, starting_position_x=0, starting_position_y=0, goal_node_x=8, goal_node_y=10)
for obs_y in range(7):
    test.add_obstacle(x=1, y=obs_y)
for obs_y in range(16):
    test.add_obstacle(x=4, y=15-obs_y)
for test_x in range(8):
    test.add_obstacle(y=12,x=4+test_x)

test.set_start_heading(0)
test.set_target_heading(90)
goal_node, start_node, all_nodes = test.convert_to_graph()

test_d_star = DStarLite(start_node=start_node,
                 goal_node=goal_node,
                 all_nodes=all_nodes,
                 cost_func=test.cost,
                 move_func=test.update_current_position_by_node)

# print("I start")

# test_d_star.main()
# print("Ididididididididi it")
visualiser = MapVisualiser(map = test, pathfinding_alg=test_d_star)
