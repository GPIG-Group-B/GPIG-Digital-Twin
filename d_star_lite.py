import heapq
from utils import euclidian_distance_from_nodes
try:
    import umath as math
except ImportError:
    import math


class Node:

    def __init__(self, predecessors : list, successors : list, pos_x, pos_y):
        self.successors = successors
        self.predecessors = predecessors
        self._rhs_val = None
        self._g_val = None
        self.pos_x = pos_x
        self.pos_y = pos_y

    def set_rhs_val(self, new_val):
        self._rhs_val = new_val

    def get_rhs_val(self):
        return self._rhs_val

    def set_g_val(self, new_val):
        self._g_val = new_val

    def get_g_val(self):
        return self._g_val




class DStarLite:


    def __init__(self, cost_func, start_node, goal_node, all_nodes, move_func):
        self.cost = cost_func
        self.start_node = start_node
        self.goal_node = goal_node
        self.all_nodes = all_nodes
        self.last_node = None
        self.priority_queue_u = None
        self.k_m = None
        self.move = move_func

    def initialise(self):
        self.priority_queue_u = DStarSet()
        self.k_m = 0
        for each_node in self.all_nodes:
            each_node.set_rhs_val(float("inf"))
            each_node.set_g_val(float("inf"))

        self.goal_node.set_rhs_val(0)
        self.priority_queue_u.insert_node_val_pair(self.goal_node, (self.h(self.start_node, self.goal_node), 0))

    def get_shortest_path_nodes(self):
        path_nodes = []
        sp_start_node = self.start_node
        while sp_start_node != self.goal_node:
            successor_val_list = [self.cost(sp_start_node, s_prime) + s_prime.get_g_val() for s_prime in sp_start_node.successors]
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
            successor_val_list = [self.cost(self.start_node, s_prime) + s_prime.get_g_val() for s_prime in self.start_node.successors]
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

    def update_edge_cost(self, u, v):
        pass

    def scan_grap_changed_edge_costs(self):
        print("Scanning")
        return True

    def h(self, from_node, to_node):
        return euclidian_distance_from_nodes(from_node, to_node)
        # return math.dist([from_node.pos_x, from_node.pos_y], [to_node.pos_x, to_node.pos_y])

    def calculate_key(self, node):
        return min(node.get_g_val(), node.get_rhs_val()) + self.h(self.start_node, node) + self.k_m, min(node.get_g_val(), node.get_rhs_val())



    def compute_shortest_path(self):
        while (self.priority_queue_u.top_key() < self.calculate_key(self.start_node)) or (self.start_node.get_rhs_val() > self.start_node.get_g_val()):
            u = self.priority_queue_u.top()
            k_old = self.priority_queue_u.top_key()
            k_new = self.calculate_key(u)
            if k_old < k_new:
                self.priority_queue_u.update(node_to_update=u, new_value=k_new)
            elif u.get_g_val() > u.get_rhs_val():
                u.set_g_val(u.get_rhs_val())
                self.priority_queue_u.delete(u)
                for s in u.predecessors:
                    if s != self.goal_node:
                        s.set_rhs_val(min(s.get_rhs_val(), self.cost(s, u) + u.get_g_val()))
                    self.update_vertex(s)
            else:
                g_old = u.get_g_val()
                u.set_g_val(float("inf"))
                for s in u.predecessors + [u]:
                    if s.get_rhs_val() == (self.cost(s, u) + g_old):
                        if s != self.goal_node:
                            min_val = None
                            for s_prime in s.successors:
                                temp = self.cost(s, s_prime) + s_prime.get_g_val()
                                if min_val is None or temp < min_val:
                                    min_val = temp
                            s.set_rhs_val(min_val)
                            # s.set_rhs_val(min([self.cost(s, s_prime) + s_prime.get_g_val() for s_prime in s.successors]))
                    self.update_vertex(s)

    def update_vertex(self, node):
        if (node.get_g_val() != node.get_rhs_val()) and self.priority_queue_u.is_node_present(node):
            print("Updated")
            self.priority_queue_u.update(node_to_update=node,
                                         new_value=self.calculate_key(node))
        elif (node.get_g_val() != node.get_rhs_val()) and not self.priority_queue_u.is_node_present(node):
            print("Insert")
            self.priority_queue_u.insert_node_val_pair(node=node, value=self.calculate_key(node=node))
        elif(node.get_g_val() == node.get_rhs_val()) and self.priority_queue_u.is_node_present(node):
            print("Delete")
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

    def insert_node_val_pair(self, node, value):
        if len(value) != 2:
            raise ValueError("Value should be of length 2")
        heapq.heappush(self, ((value[0],value[1], self.get_tiebreaker_index(value)), node))


    def is_node_present(self, node):
        for each_value, each_node in self:
            if node == each_node:
                return True
        return False

    def get_tiebreaker_index(self, value):
        n = 0
        for (prio_0, prio_1, tiebreaker_val), each_node in self:
            if value[0] == prio_0 and value[1] == prio_1:
                n += tiebreaker_val + 1
        return n

    #TODO: Update to account for removal of tiebreakers properly
    def update(self, node_to_update, new_value = None):
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
            # pass
            # print(value, node)
            self.insert_node_val_pair(node=node, value=value)


    def delete(self, node):
        # print("======== DELETION =====")
        # print(self)
        # for val, node_2 in self:
        #     print(f"Node : {node_2} | Value : {val}| pos X : {node_2.pos_x} | Pos Y : {node_2.pos_y}")
        # print(f"Node being deleted : {node} | Pos X : {node.pos_x} | Pos Y {node.pos_y}")
        # print("======== DELETION =====")
        self.update(node_to_update=node, new_value=None)

if __name__ == '__main__':
    pass


