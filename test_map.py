from map import Map
from d_star_lite import DStarLite

def cost_func(x,y):
    return 1

test = Map(size_x=3, size_y=3, resolution=0.5, starting_position_x=0, starting_position_y=0, goal_node_x=3, goal_node_y=3)
# test.add_impassable_rock_by_angle_distance(0, 1.0)
goal_node, start_node, all_nodes = test.convert_to_graph()

test = DStarLite(start_node=start_node,
                 goal_node=goal_node,
                 all_nodes=all_nodes,
                 cost_func=cost_func)
test.main()