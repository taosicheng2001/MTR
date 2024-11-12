from Topology import Topology, Mesh
from Router import RouterNode, Link, XYRouting
from typing import Optional
import numpy as np

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

    def DFS(self, checking_list, reachable_list, matrix = None):
        if len(checking_list) == 0:
            return

        cur_link = checking_list.pop(0)
        reachable_list.append(cur_link)
        for link in self.cdg_edges:
            head_link = link[0] # N13_N12  X_N13
            tail_link = link[1] # N12_N8   N13_N12

            if cur_link != head_link:
                continue
            if tail_link.split('_')[1] == head_link.split('_')[0]:
                continue

            if matrix is not None:
                cur_node_0 = tail_link.split('_')[0]
                cur_node_1 = tail_link.split('_')[1]
                if head_link.split('_')[0] == "X":
                    matrix[int(cur_node_1[1:])] = min(1, matrix[int(cur_node_1[1:])])
                if cur_node_0 != "X" and cur_node_1 != "X" :
                    if matrix[int(cur_node_1[1:])] > matrix[int(cur_node_0[1:])]+1:
                        matrix[int(cur_node_1[1:])] = matrix[int(cur_node_0[1:])] + 1


            checking_list.append(tail_link)
            reachable_list.append(tail_link)

        self.DFS(checking_list, reachable_list, matrix)
    
    def DFS_back(self, checking_list, reachable_list, matrix = None):
        if len(checking_list) == 0:
            return

        cur_link = checking_list.pop(0)
        reachable_list.append(cur_link)
        for link in self.cdg_edges:
            head_link = link[0] # N0_N1 N4_N0
            tail_link = link[1] # N1_X  N0_N1

            if cur_link != tail_link:
                continue
            if tail_link.split('_')[1] == head_link.split('_')[0]:
                continue
            
            if matrix is not None:
                cur_node_0 = head_link.split('_')[0]
                cur_node_1 = head_link.split('_')[1]
                if tail_link.split('_')[1] == "X":
                    matrix[int(cur_node_0[1:])] = min(1, matrix[int(cur_node_0[1:])])
                if cur_node_0 != "X" and cur_node_1 != "X" :
                    if matrix[int(cur_node_0[1:])] > matrix[int(cur_node_1[1:])]+1:
                        matrix[int(cur_node_0[1:])] = matrix[int(cur_node_1[1:])] + 1

            checking_list.append(head_link)
            reachable_list.append(head_link)

        self.DFS_back(checking_list, reachable_list, matrix)

    def get_Neighbor(self, node):
        rt = []
        for link in self.cdg_edges:
            head_link = link[0] # X_N1 
            if head_link.split('_')[0] == node:
                rt.append(head_link)
        return rt

    def isConnected(self, reachable_list, br = ""):

        dest_nodes = []
        for rl in reachable_list:
            dest_node = rl.split('_')[1]
            dest_nodes.append(dest_node)

        unique = set(list(dest_nodes))
        return len(unique) == 17

    def calConnected(self, reachable_list, br = ""):

        dest_nodes = []
        for rl in reachable_list:
            dest_node = rl.split('_')[1]
            dest_nodes.append(dest_node)

        unique = set(list(dest_nodes))
        if "X" in unique:
            unique.remove("X")
        return len(unique)

    def calConnected_back(self, reachable_list, br = ""):

        dest_nodes = []
        for rl in reachable_list:
            dest_node = rl.split('_')[0]
            dest_nodes.append(dest_node)

        unique = set(list(dest_nodes))
        if "X" in unique:
            unique.remove("X")
        return len(unique)

    def evaluate(self, abstract_node, brs):
        links = self.topology.links
        nodes = self.topology.nodes
        nodes.append(abstract_node)

        InMatrix = np.full(16, 50)
        OutMatrix = np.full(16, 50)

        InR = 0
        for br in brs:
            InMatrix[br] = 0
            checking_list = ["X_N"+str(br)]
            reachable_list = []
            self.DFS(checking_list, reachable_list, InMatrix)
            InR += self.calConnected(reachable_list, br)

        OutR = 0
        for br in brs:
            OutMatrix[br] = 0
            checking_list = ["N"+str(br)+"_X"]
            reachable_list = []
            self.DFS_back(checking_list, reachable_list, OutMatrix)
            OutR += self.calConnected_back(reachable_list, br)

        ave_InR = float(InR) / (16 * 4)
        ave_OutR = float(OutR) / (16 * 4)
        ave_InD = float(np.sum(InMatrix)) / 16
        ave_OutD = float(np.sum(OutMatrix)) / 16

        return (ave_InD+ ave_OutD) / (ave_InR+ave_OutR)





if __name__ == "__main__":
    topo = Mesh(n_nodes=16, n_cols=4, n_rows=4)
    routing = XYRouting()
    network = Network(topo, routing)
