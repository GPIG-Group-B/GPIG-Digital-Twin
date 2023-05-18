import math

from d_star_lite import Node


class Map:


    def __init__(self,
                 size_x : float,
                 size_y : float,
                 resolution : float,
                 starting_position_x : int,
                 starting_position_y : int,
                 goal_node_x : int,
                 goal_node_y : int):
        # Resolution in meters
        # Size X and size Y in meters
        self._grid_size_x = size_x // resolution
        self._grid_size_y = size_y // resolution
        self._resolution = resolution
        self._goal_node_x = goal_node_x
        self._goal_node_y = goal_node_y
        if not self._grid_size_x.is_integer():
            raise ValueError("Map width must be wholly divisible by resolution")
        if not self._grid_size_y.is_integer():
            raise ValueError("Map height must be wholly divisible by resolution")

        self._grid_size_x, self._grid_size_y = int(self._grid_size_x), int(self._grid_size_y)
        self._grid = self._make_grid_array()
        self._current_pos_x = starting_position_x
        self._current_pos_y = starting_position_y
        self._update_current_position(x = self._current_pos_x,
                                      y = self._current_pos_y)
        self.set_goal_pos(x=self._goal_node_x,
                          y=self._goal_node_y)
        self.pretty_print_grid()


    def set_goal_pos(self, x,y):
        self._grid[self._grid_size_y - y - 1][x] = GoalTile(pos_x=x, pos_y=y)
    def _update_current_position(self, x, y):
        self._grid[self._grid_size_y - self._current_pos_y - 1][self._current_pos_x] = EmptyTile(pos_x=x, pos_y=y)
        self._grid[self._grid_size_y - y - 1][x] = RoverTile(pos_x=x, pos_y=y)
        self._current_pos_x = x
        self._current_pos_y = y

    def _make_grid_array(self):
        return [[EmptyTile(pos_x=x, pos_y=y) for x in range(self._grid_size_x)] for y in range(self._grid_size_y)]

    def pretty_print_grid(self):
        print("\n")
        print("================================")
        print("\n")

        for each_row in self._grid:
            print(str(each_row).replace(", ", ""))
        print("\n")
        print("================================")
        print("\n")

    def add_impassable_rock_by_angle_distance(self, angle, distance):

        object_position_x = math.sin(angle) * distance
        object_position_y = math.cos(angle) * distance
        object_grid_position_x = math.floor(object_position_x / self._resolution)
        object_grid_position_y = math.floor(object_position_y / self._resolution)
        self._grid[self._grid_size_y - object_grid_position_y - 1][object_grid_position_x] = ImpassableRockTile(pos_x=object_position_x, pos_y=object_grid_position_y)
        self.pretty_print_grid()


    def _get_position_as_distance(self, x , y):
        return x * self._resolution, y * self._resolution

    def convert_to_graph(self):
        for row_id in range(self._grid_size_y):
            for col_id in range(self._grid_size_x):
                center_node = self.get_grid_node(x=col_id, y = row_id)
                for x_delta in (-1,1):
                    for y_delta in (-1, 1):
                        cell_col_id = col_id + x_delta
                        cell_row_id = row_id + y_delta
                        if self._grid_size_y > cell_row_id >= 0:
                            if self._grid_size_x > cell_col_id >= 0:
                                current_cell = self.get_grid_node(x=cell_col_id,
                                                                  y=cell_row_id)
                                center_node.successors.append(current_cell)
                                center_node.predecessors.append(current_cell)
                                current_cell.successors.append(center_node)
                                current_cell.predecessors.append(center_node)
        all_nodes = [cell.node for y in self._grid for cell in y]
        return self.get_grid_node(x=self._goal_node_x, y = self._goal_node_x), self.get_grid_node(x=self._current_pos_x, y = self._current_pos_y), all_nodes
    def get_grid_node(self,x,y):
        return self._grid[self._grid_size_y - y - 1][x].node

class Tile():

    def __init__(self, type_id, type_name ,pos_x, pos_y):
        self.type_id = type_id
        self.type_name = type_name
        self.node = Node(predecessors=[], successors=[], pos_x=pos_x, pos_y=pos_y)

    def __str__(self):
        return f"[{self.type_name}]"
    def __repr__(self):
        return f"[{self.type_name}]"

class EmptyTile(Tile):

    def __init__(self, pos_x, pos_y):
        super().__init__(type_id = 0, type_name = "Empty", pos_x=pos_x, pos_y=pos_y)

class RoverTile(Tile):

    def __init__(self, pos_x, pos_y):
        super().__init__(type_id = 1, type_name = "Rover", pos_x=pos_x, pos_y=pos_y)

class ImpassableRockTile(Tile):
    def __init__(self, pos_x, pos_y):
        super().__init__(type_id = 2, type_name = "Rock", pos_x=pos_x, pos_y=pos_y)


class GoalTile(Tile):
    
    def __init__(self, pos_x, pos_y):
        super().__init__(type_id = 2, type_name="Goal", pos_x=pos_x, pos_y=pos_y)

if __name__ == "__main__":
    test = Map(size_x=3, size_y=3, resolution=0.5, starting_position_x=0, starting_position_y=0, goal_node_x=3, goal_node_y=3)
    # test.add_impassable_rock_by_angle_distance(0, 1.0)
    goal_node, start_node, all_nodes = test.convert_to_graph()
