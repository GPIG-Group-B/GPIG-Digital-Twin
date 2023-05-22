from d_star_lite import Node, DStarLite, euclidian_distance_from_nodes
try:
    import umath as math
except ImportError:
    import math
    import time
    import pygame

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
        self._grid_size_x = size_x / resolution
        self._grid_size_y = size_y / resolution
        self._resolution = resolution
        self._goal_node_x = goal_node_x
        self._goal_node_y = goal_node_y
        if not self._is_int(self._grid_size_x):
            raise ValueError("Map width must be wholly divisible by resolution")
        if not self._is_int(self._grid_size_y):
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

    def get_resolution(self):
        return self._resolution

    @staticmethod
    def _is_int(num):
        return num % 1 == 0

    def get_grid_size_y(self):
        return self._grid_size_y

    def get_grid_size_x(self):
        return self._grid_size_x

    def get_grid(self):
        return self._grid


    def set_goal_pos(self, x,y):
        self._grid[y][x] = GoalTile(pos_x=x, pos_y=y)

    def _update_current_position(self, x, y):
        self._grid[self._current_pos_y][self._current_pos_x] = EmptyTile(pos_x=self._current_pos_x, pos_y=self._current_pos_y)
        self._grid[y][x] = RoverTile(pos_x=x, pos_y=y)
        self._current_pos_x = x
        self._current_pos_y = y

    def update_current_position_by_node(self, node : Node):
        self._update_current_position(x=node.pos_x, y=node.pos_y)
        self.pretty_print_grid()
    def _make_grid_array(self):
        return [[EmptyTile(pos_x=x, pos_y=y) for x in range(self._grid_size_x)] for y in range(self._grid_size_y)]

    def pretty_print_grid(self):
        return
        print("\n")
        print("================================")
        print("\n")

        for each_row in self._grid:
            print(str(each_row).replace(", ", ""))
        print("\n")
        print("================================")
        print("\n")

    # def add_impassable_rock_by_angle_distance(self, angle, distance):
    #
    #     object_position_x = math.sin(angle) * distance
    #     object_position_y = math.cos(angle) * distance
    #     object_grid_position_x = math.floor(object_position_x / self._resolution)
    #     object_grid_position_y = math.floor(object_position_y / self._resolution)
    #     self._grid[object_grid_position_y][object_grid_position_x] = ObstacleTile(pos_x=object_position_x, pos_y=object_grid_position_y)
    #     self.pretty_print_grid()

    def add_obstacle(self, x, y):
        self._grid[y][x] = ObstacleTile(pos_x=x,pos_y=y)


    def _get_position_as_distance(self, x , y):
        return x * self._resolution, y * self._resolution

    def convert_to_graph(self):
        for row_id in range(self._grid_size_y):
            for col_id in range(self._grid_size_x):
                center_node = self.get_grid_node(x=col_id, y = row_id)
                for x_delta, y_delta in [(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0)]:
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
        return self.get_grid_node(x=self._goal_node_x, y = self._goal_node_y), self.get_grid_node(x=self._current_pos_x, y = self._current_pos_y), all_nodes
    def get_grid_node(self,x,y):
        return self._grid[y][x].node

    def cost(self, u,v):
        u_cell = self._grid[u.pos_y][u.pos_x]
        v_cell = self._grid[v.pos_y][v.pos_x]
        if isinstance(u_cell, (EmptyTile, GoalTile, RoverTile)) and isinstance(v_cell, (EmptyTile, GoalTile, RoverTile)):
            return euclidian_distance_from_nodes(u, v)
        else:
            return float("inf")

class Tile():

    def __init__(self, type_id, type_name ,pos_x, pos_y, colour = (255,255,255)):
        self.type_id = type_id
        self.type_name = type_name
        self.colour = colour
        self.node = Node(predecessors=[], successors=[], pos_x=pos_x, pos_y=pos_y)

    def __str__(self):
        return f"[{self.type_name}]"
    def __repr__(self):
        return f"[{self.type_name}]"

class EmptyTile(Tile):

    def __init__(self, pos_x, pos_y):
        super().__init__(type_id = 0, type_name = "Empty", pos_x=pos_x, pos_y=pos_y, colour=(125,125,125))

class RoverTile(Tile):

    def __init__(self, pos_x, pos_y):
        super().__init__(type_id = 1, type_name = "Rover", pos_x=pos_x, pos_y=pos_y, colour=(255,255,255))

class ObstacleTile(Tile):
    def __init__(self, pos_x, pos_y):
        super().__init__(type_id = 2, type_name = "Rock", pos_x=pos_x, pos_y=pos_y, colour=(0,0,0))


class GoalTile(Tile):
    
    def __init__(self, pos_x, pos_y):
        super().__init__(type_id = 2, type_name="Goal", pos_x=pos_x, pos_y=pos_y, colour=(0,255,0))

class MapVisualiser():

    def __init__(self, map : Map, pathfinding_alg : DStarLite):
        self._map = map
        self._pathfinding_alg = pathfinding_alg
        pathfinding_alg.move = self.move
        self._map_grid_size_x = self._map.get_grid_size_x()
        self._map_grid_size_y = self._map.get_grid_size_y()



        pygame.init()
        window_height, window_width = pygame.display.Info().current_h, pygame.display.Info().current_w
        self._tile_size = min((window_width - 100) // self._map_grid_size_x, (window_height - 100) // self._map_grid_size_y)
        self._main_window_height = self._tile_size * self._map_grid_size_y
        self._main_window_width = self._tile_size * self._map_grid_size_x
        self._main_screen = pygame.display.set_mode((self._main_window_width, self._main_window_height))
        self._draw_grid()
        self._pathfinding_alg.main()
        running = True
        while running:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting")
                    running = False
        pygame.quit()

    def move(self, node):
        time.sleep(0.1)
        self._map.update_current_position_by_node(node)
        shortest_path_list = self._pathfinding_alg.get_shortest_path_nodes()
        self._draw_grid()
        self.draw_shortest_path(shortest_path_list)


    def draw_shortest_path(self, shortest_path_nodes):
        for node in shortest_path_nodes:
            if node != self._pathfinding_alg.goal_node:
                x, y = node.pos_x, node.pos_y
                self._draw_tile(x=x, y=y, colour=(0,0,255))
        pygame.display.update()

    def _draw_tile(self, x, y, colour):
        tile_rect = pygame.Rect(x * self._tile_size, y * self._tile_size, self._tile_size, self._tile_size)
        pygame.draw.rect(self._main_screen, colour, tile_rect)
        # border_rect = pygame.Rect((x * self._tile_size), (y * self._tile_size), self._tile_size, self._tile_size )
        # pygame.draw.rect(self._main_screen, (125,255,255), border_rect, width=10)

    def _draw_grid(self, shortest_path_list = None):
        if self._tile_size is None:
            raise Exception("Attemping to draw grid when UI is disabled")
        for y in range(self._map_grid_size_y):
            for x in range(self._map_grid_size_x):
                self._draw_tile(x=x, y=y, colour=self._map.get_grid()[y][x].colour)
        pygame.display.update()



if __name__ == "__main__":
    test = Map(size_x=3, size_y=3, resolution=0.1, starting_position_x=1, starting_position_y=1, goal_node_x=3, goal_node_y=3)
    # test.add_impassable_rock_by_angle_distance(0, 1.0)
    goal_node, start_node, all_nodes = test.convert_to_graph()


