import math
from cgitb import reset


class Map:


    def __init__(self,
                 size_x : float,
                 size_y : float,
                 resolution : float,
                 starting_position_x : int,
                 starting_position_y : int):
        # Resolution in meters
        # Size X and size Y in meters
        self._grid_size_x = size_x // resolution
        self._grid_size_y = size_y // resolution
        self._resolution = resolution
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
        self.pretty_print_grid()

    def _update_current_position(self, x, y):
        self._grid[self._grid_size_y - self._current_pos_y - 1][self._current_pos_x] = EmptyTile()
        self._grid[self._grid_size_y - y - 1][x] = RoverTile()
        self._current_pos_x = x
        self._current_pos_y = y

    def _make_grid_array(self):
        return [[EmptyTile() for _ in range(self._grid_size_x)] for _ in range(self._grid_size_y)]

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
        self._grid[self._grid_size_y - object_grid_position_y - 1][object_grid_position_x] = ImpassableRockTile()
        self.pretty_print_grid()


    def _get_position_as_distance(self, x , y):
        return x * self._resolution, y * self._resolution


class Tile():

    def __init__(self, type_id, type_name):
        self.type_id = type_id
        self.type_name = type_name

    def __str__(self):
        return f"[{self.type_name}]"
    def __repr__(self):
        return f"[{self.type_name}]"

class EmptyTile(Tile):

    def __init__(self):
        super().__init__(type_id = 0, type_name = "Empty")

class RoverTile(Tile):

    def __init__(self):
        super().__init__(type_id = 1, type_name = "Rover")

class ImpassableRockTile(Tile):
    def __init__(self):
        super().__init__(type_id = 2, type_name = "Rock")


if __name__ == "__main__":
    test = Map(size_x=3, size_y=3, resolution=0.5, starting_position_x=0, starting_position_y=0)
    test.add_impassable_rock_by_angle_distance(0, 1.0)
