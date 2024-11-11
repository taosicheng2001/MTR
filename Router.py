# author: taosicheng
# date: 2024.11.11

from typing import Optional

class RouterNode(object):
    name = ""
    id = 0
    ports = []

    def __init__(self, name, id) -> None:
        self.name = name
        self.id = id
        self.ports = []

class Link(object):
    name = ""
    n0:  Optional[RouterNode] = None
    n1:  Optional[RouterNode] = None

    def __init__(self, n0, n1):
        self.name = n0.name + "_" + n1.name
        self.n0 = n0
        self.n1 = n1

class XYRouting(object):

    def __init__(self):
        pass

    def next_hop(self, src_node, dest_node, mesh):
        src = src_node.id
        dest = dest_node.id
        src_x, src_y = src % mesh.n_cols, src // mesh.n_cols
        dest_x, dest_y = dest % mesh.n_cols, dest // mesh.n_cols

        if dest_x > src_x:
            return "R"
        if dest_x < src_y:
            return "L"
        if dest_y > src_y:
            return "D"
        if dest_y < src_y:
            return "U"
        return "F"
