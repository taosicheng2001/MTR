from Topology import Topology, Mesh
from Router import RouterNode, Link, XYRouting
from typing import Optional

class Network(object):
    topology: Optional[Topology] = None
    routing: Optional[XYRouting] = None
    cdg = []

    def __init__(self, topology, routing):
        self.topology = topology
        self.routing = routing
        self.gen_cdg()

    def gen_cdg(self):
        self.cdg = []
        for head_link in self.topology.links:
            for tail_link in self.topology.links:
                head_head_node = self.topology.nodes[int(head_link.name.split('_')[0][1:])]
                tail_head_node = self.topology.nodes[int(head_link.name.split('_')[1][1:])]
                head_tail_node = self.topology.nodes[int(tail_link.name.split('_')[0][1:])]
                tail_tail_node = self.topology.nodes[int(tail_link.name.split('_')[1][1:])]

                if tail_head_node != head_tail_node:
                    continue
                if head_head_node == tail_tail_node:
                    continue
                else:
                    port0 = self.routing.next_hop(head_head_node, head_tail_node, self.topology)
                    port1 = self.routing.next_hop(head_tail_node, tail_tail_node, self.topology)
                    if port0 in ["U", "D"] and port1 in ["L", "R"]:
                        continue
                    else:
                        self.cdg.append([head_link.name + "-" + tail_link.name])




if __name__ == "__main__":
    topo = Mesh(n_nodes=16, n_cols=4, n_rows=4)
    routing = XYRouting()
    network = Network(topo, routing)
