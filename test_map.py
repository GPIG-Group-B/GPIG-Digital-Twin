import math

from map import Map, EmptyTile, RoverTile, ImpassableRockTile, GoalTile
from d_star_lite import DStarLite

# def cost_func(x,y):
    # if not isinstance(x, (EmptyTile,GoalTile, RoverTile)) or not isinstance(y, (EmptyTile,GoalTile)):
    #     return float("inf")
    # else:
    # return math.dist([x.pos_x, x.pos_y], [y.pos_x, y.pos_y])

test = Map(size_x=3, size_y=3, resolution=0.5, starting_position_x=0, starting_position_y=0, goal_node_x=5, goal_node_y=5)
# test.add_impassable_rock_by_angle_distance(0, 1.0)
goal_node, start_node, all_nodes = test.convert_to_graph()

test = DStarLite(start_node=start_node,
                 goal_node=goal_node,
                 all_nodes=all_nodes,
                 cost_func=test.cost,
                 move_func=test.update_current_position_by_node)
test.main()