from Topology import Topology, Mesh
from Router import RouterNode, Link, XYRouting
from typing import Optional

class Network(object):
    topology: Optional[Topology] = None
    routing: Optional[XYRouting] = None
    cdg_edges = []
    cdg_vertexs = []


    def __init__(self, topology, routing):
        self.topology = topology
        self.routing = routing
        self.gen_cdg()

    def get_Node(self, link, abstract_node):
        head_node = link.name.split('_')[0]
        tail_node = link.name.split('_')[1]


        if "X" in head_node:
            return [abstract_node, self.topology.nodes[int(tail_node[1:])]]
        if "X" in tail_node:
            return [self.topology.nodes[int(head_node[1:])], abstract_node]
        return [self.topology.nodes[int(head_node[1:])], self.topology.nodes[int(tail_node[1:])]]

    def gen_cdg(self, abstract_node = None, forbidden_list = []):
        self.cdg_edges = []
        self.cdg_vertexs = []
        cdg_vertexs = []
        for head_link in self.topology.links:
            for tail_link in self.topology.links:

                # Skip link pair in forbidden list
                skip_flag = False
                for forbidden_link_pair in forbidden_list:
                    if forbidden_link_pair[0] == head_link and forbidden_link_pair[1] == tail_link:
                        skip_flag = True
                        break

                if skip_flag:
                    continue

                # Extract all router nodes
                if abstract_node is None:
                    head_head_node = self.topology.nodes[int(head_link.name.split('_')[0][1:])]
                    tail_head_node = self.topology.nodes[int(head_link.name.split('_')[1][1:])]
                    head_tail_node = self.topology.nodes[int(tail_link.name.split('_')[0][1:])]
                    tail_tail_node = self.topology.nodes[int(tail_link.name.split('_')[1][1:])]
                else:
                    head_head_node, tail_head_node = self.get_Node(head_link, abstract_node)
                    head_tail_node, tail_tail_node = self.get_Node(tail_link, abstract_node)

                # Intermedia node must be the same
                if tail_head_node != head_tail_node:
                    continue
                # A ->B and B -> A is not allowed
                if head_head_node == tail_tail_node:
                    continue
                else:
                    node_list = [head_head_node, head_tail_node, tail_tail_node]
                    port0 = self.routing.next_hop(head_head_node, tail_head_node, self.topology)
                    port1 = self.routing.next_hop(head_tail_node, tail_tail_node, self.topology)

                    # Remove XY routing limitation
                    if port0 in ["U", "D"] and port1 in ["L", "R"]:
                        continue
                    else:
                        self.cdg_edges.append([head_link.name, tail_link.name])
                        cdg_vertexs.append(head_link.name)
                        cdg_vertexs.append(tail_link.name)

        # Unique the vertexs
        self.cdg_vertexs = list(set(cdg_vertexs))

    def evaluate(self, abstract_node, brs):
        links = self.topology.links
        nodes = self.topology.nodes
        nodes.append(abstract_node)

        InR = 0
        OutR = 0
        for br in brs:
            break


        



if __name__ == "__main__":
    topo = Mesh(n_nodes=16, n_cols=4, n_rows=4)
    routing = XYRouting()
    network = Network(topo, routing)
