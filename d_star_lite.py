import heapq

try:
    import umath as math
except ImportError:
    import math


class Node:

    def __init__(self,
                 predecessors: list,
                 successors: list,
                 pos_x,
                 pos_y):
        self.successors = successors
        self.predecessors = predecessors
        self._rhs_val = None
        self._g_val = None
        self.pos_x = pos_x
        self.pos_y = pos_y

    def __str__(self) -> str:
        return f"---- Node ----\nPosX:{self.pos_x}\nPosY{self.pos_y}\nTotals:\n\tPredecessors:{len(self.predecessors)}\n\tSuccessors:{len(self.successors)}\n---- End Node ----"
    def set_rhs_val(self,
                    new_val):
        self._rhs_val = new_val

    def get_rhs_val(self):
        return self._rhs_val

    def set_g_val(self,
                  new_val):
        self._g_val = new_val

    def get_g_val(self):
        return self._g_val


def euclidian_distance_from_nodes(node_1: Node,
                                  node_2: Node):
    return math.sqrt((node_1.pos_x - node_2.pos_x) ** 2 + (node_1.pos_y - node_2.pos_y) ** 2)


class DStarLite:

    def __init__(self,
                 cost_func,
                 start_node,
                 goal_node,
                 all_nodes,
                 move_func):
        self.cost = cost_func
        self.start_node = start_node
        self.goal_node = goal_node
        self.all_nodes = all_nodes
        self.last_node = None
        self.priority_queue_u = None
        self.k_m = None
        self.move = move_func
        self.prev_node = None
        self.node_history = []
        self.rover_start_angle = 180

    def initialise(self):
        self.priority_queue_u = DStarSet()
        self.k_m = 0
        for each_node in self.all_nodes:
            each_node.set_rhs_val(float("inf"))
            each_node.set_g_val(float("inf"))

        self.goal_node.set_rhs_val(0)
        self.priority_queue_u.insert_node_val_pair(self.goal_node,
                                                   (self.h(self.start_node,
                                                           self.goal_node), 0))

    def get_shortest_path_nodes(self):
        path_nodes = []
        sp_start_node = self.start_node
        while sp_start_node != self.goal_node:
            successor_val_list = [self.cost(sp_start_node,
                                            s_prime) + s_prime.get_g_val() for s_prime in sp_start_node.successors]
            sp_start_node = sp_start_node.successors[successor_val_list.index(min(successor_val_list))]
            path_nodes.append(sp_start_node)
        return path_nodes


    def main(self):
        self.last_node = self.start_node
        self.initialise()
        self.compute_shortest_path()
        while self.start_node != self.goal_node:
            if self.start_node.get_rhs_val() == float("inf"):
                raise Exception("No computable path")
            successor_val_list = [self.cost(self.start_node,
                                            s_prime) + s_prime.get_g_val() for s_prime in self.start_node.successors]
            two_nodes_ahead = self.get_shortest_path_nodes()[1]
            if two_nodes_ahead:
                angle_to_move = int(math.degrees(math.atan2(two_nodes_ahead.pos_x - self.start_node.pos_x,
                                                            two_nodes_ahead.pos_y - self.start_node.pos_y)))
                if angle_to_move == 45:
                    self.start_node = two_nodes_ahead
                else:
                    self.start_node = self.start_node.successors[successor_val_list.index(min(successor_val_list))]
            self.move(self.start_node)
            # changed_edges = self.scan_grap_changed_edge_costs()
            # if len(changed_edges) != 0:
            #     self.k_m = self.k_m + self.h(self.last_node, self.start_node)
            #     self.last_node = self.start_node
            #     for each_directed_edge in changed_edges:
            #         u, v = each_directed_edge
            #         c_old = self.cost(u,v)
            #         self.update_edge_cost(u,v)
            #         if c_old > self.cost(u, v):
            #             if u != self.goal_node:
            #                 u.set_rhs_val(min(u.get_rhs_val, self.cost(u, v) + v.get_g_val()))
            #         elif u.get_rhs_val() == c_old + v.get_g_val():
            #             if u != self.goal_node:
            #                 u.get_rhs_val(min([self.cost(u, s_prime) + s_prime.get_g_val() for s_prime in u.successors]))
            #         self.update_vertex(u)
            #     self.compute_shortest_path()
        print("I finished")

    def update_edge_cost(self,
                         u,
                         v):
        pass

    def scan_grap_changed_edge_costs(self):
        print("Scanning")
        return True

    def h(self,
          from_node,
          to_node):
        return euclidian_distance_from_nodes(from_node,
                                             to_node)

    def calculate_key(self,
                      node):
        return min(node.get_g_val(),
                   node.get_rhs_val()) + self.h(self.start_node,
                                                node) + self.k_m, min(node.get_g_val(),
                                                                      node.get_rhs_val())

    def get_possible_move_cells(self,heading):
        
        output = []
        offsets = [(-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]
        if( heading is None):
            print("Got a null Value!!!")
            return offsets
        heading_offset = [315, 0, 45, 135, 180, 225]
        for i in range(3):## Backwards
            output.append(offsets[(int(((heading%360)/45)+0.5)+i)%8])

        ## Forwards
        output.append(offsets[(int(((heading % 360) / 45) + 0.5) + 4) % 8])
        output.append(offsets[(int(((heading % 360) / 45) + 0.5) + 1 + 4) % 8])
        output.append(offsets[(int(((heading % 360) / 45) + 0.5) + 2 + 4) % 8])

        return output
        ## Filtering is now down in graph creation
        # return output

    def compute_shortest_path(self):
        while (self.priority_queue_u.top_key() < self.calculate_key(self.start_node)) or (self.start_node.get_rhs_val() > self.start_node.get_g_val()):
            u: Node = self.priority_queue_u.top()
            k_old = self.priority_queue_u.top_key()
            k_new = self.calculate_key(u)
            if k_old < k_new:
                self.priority_queue_u.update(node_to_update=u,
                                             new_value=k_new)
            elif u.get_g_val() > u.get_rhs_val():
                u.set_g_val(u.get_rhs_val())
                self.priority_queue_u.delete(u)

                """
                Nodes

                C - current
                P - previous
                N - next

                P -> C -> N

                The angle between P and C reduces the possible set of nodes (N) available
                """
                ## Calculating the angle from the prev node to my node
                ## Tan = X/Y
                ## Heading = atan(dx/dy)
                ## dx = last_node_x - current_node_x
                ## dy = last_node_y - current_node_y

                _min = float("inf")
                _min_succ = None
                for succ in u.successors:
                    if succ.get_rhs_val() < _min:
                        _min = succ.get_rhs_val()
                        _min_succ = succ

                self.prev_node = _min_succ
                if self.prev_node is None or u == self.goal_node:
                    prev_heading = None  ##TODO: CHANGE THIS TO MATCH THE TARGET NODE HEADING
                else:
                    last_node: Node = self.prev_node
                    if last_node.pos_y - u.pos_y != 0:
                        prev_heading = math.degrees(math.atan(abs(last_node.pos_x - u.pos_x) / (last_node.pos_y - u.pos_y))) % 180
                        if last_node.pos_x - u.pos_x < 0:
                            prev_heading = 360 - prev_heading
                    else:
                        prev_heading = (90 * ((last_node.pos_x - u.pos_x) / abs((last_node.pos_x - u.pos_x)))) % 360

                # if self.prev_node is not None:
                #     print(u.pos_x,
                #           u.pos_y,
                #           prev_heading,
                #           "from",
                #           self.prev_node.pos_x,
                #           self.prev_node.pos_y)
                # if u is self.start_node:
                #     prev_heading = self.rover_start_angle
                #     print("Start Node!!!")
                #     print(u)
                
                if(prev_heading is None):
                            print(u)
                            print("START Predecessors")
                            for s in u.predecessors:
                                print(s)
                            print("END Predecessors")
                print(u.pos_x,u.pos_y,"\t",self.get_possible_move_cells(prev_heading))         
                for s in u.predecessors:
                    if s != self.goal_node:
                        if (int(s.pos_x - u.pos_x), int(s.pos_y - u.pos_y)) in self.get_possible_move_cells(prev_heading):
                            ##print("\t",s.pos_x,s.pos_y)
                            s.set_rhs_val(min(s.get_rhs_val(),self.cost(s,u) + u.get_g_val()))
                    self.update_vertex(s)
            else:
                g_old = u.get_g_val()
                u.set_g_val(float("inf"))
                for s in u.predecessors + [u]:
                    if s.get_rhs_val() == (self.cost(s,
                                                     u) + g_old):
                        if s != self.goal_node:
                            s.set_rhs_val(min([self.cost(s, s_prime) + s_prime.get_g_val() for s_prime in s.successors]))
                    self.update_vertex(s)

    def update_vertex(self,
                      node):
        if (node.get_g_val() != node.get_rhs_val()) and self.priority_queue_u.is_node_present(node):
            self.priority_queue_u.update(node_to_update=node,
                                         new_value=self.calculate_key(node))
        elif (node.get_g_val() != node.get_rhs_val()) and not self.priority_queue_u.is_node_present(node):
            self.priority_queue_u.insert_node_val_pair(node=node,
                                                       value=self.calculate_key(node=node))
        elif (node.get_g_val() == node.get_rhs_val()) and self.priority_queue_u.is_node_present(node):
            self.priority_queue_u.delete(node=node)


class DStarSet(list):

    def __init__(self):
        super().__init__()
        heapq.heapify(self)

    def top_key(self):
        if len(self) == 0:
            return float("inf"), float("inf")
        else:
            return self[0][0]

    def top(self):
        return self[0][1]

    def insert_node_val_pair(self,
                             node,
                             value):
        if len(value) != 2:
            raise ValueError(f"Length of value needs to be 2. Got : {value}")
        heapq.heappush(self,
                       ((value[0], value[1], self.get_tiebreaker_index(value)), node))

    def is_node_present(self,
                        node):
        for each_value, each_node in self:
            if node == each_node:
                return True
        return False

    def get_tiebreaker_index(self,
                             value):
        n = 0
        for (prio_0, prio_1, tiebreaker_val), each_node in self:
            if value[0] == prio_0 and value[1] == prio_1:
                n += tiebreaker_val + 1
        return n

    # TODO: Update to account for removal of tiebreakers properly
    def update(self,
               node_to_update,
               new_value=None):
        found_node = False
        to_re_add = []
        for _ in range(len(self)):
            value, node = heapq.heappop(self)
            if node == node_to_update:
                if found_node:
                    raise ValueError("Multiple of the same node in queue")
                found_node = True
                if new_value is not None:
                    to_re_add.append(((value[0], value[1]), node))
            else:
                to_re_add.append(((value[0], value[1]), node))
        if not found_node:
            raise ValueError(f"Node : {found_node} could not be found in heap")
        for value, node in to_re_add:
            self.insert_node_val_pair(node=node,
                                      value=value)

    def delete(self,
               node):
        self.update(node_to_update=node,
                    new_value=None)


if __name__ == '__main__':
    pass
