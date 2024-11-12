import networkx as nx
import copy
import numpy as np
from tqdm import tqdm
from math import pow
from graphviz import Graph, Digraph
from Topology import Topology, Mesh
from Router import RouterNode, Link, XYRouting
from Network import Network

min_tr = 12
min_eva = 100

def save_graph(nodes, links, view=False, dot=None, render=False):
    mesh_dot = dot or Graph()
    for node in nodes:
        mesh_dot.node(node, shape="box")
    for link in links:
        mesh_dot.edge(link[0], link[1])
    if render:
        mesh_dot.render(
            "Die" + self.name + "_Topology", format="png", directory="./image"
        )
    if view:
        mesh_dot.view()

def setTurn(network, abstract_node, brs , bt, pt, start, end):
    global min_tr
    if len(pt) > min_tr:
        return

    if start >= end:
        return

    # Update CDG
    new_network = copy.deepcopy(network)
    new_network.gen_cdg(abstract_node, pt)

    G = nx.DiGraph()
    G.add_nodes_from(new_network.cdg_vertexs)
    G.add_edges_from(new_network.cdg_edges)
    cycles = list(nx.simple_cycles(G))
    

    # Check Cycle
    if len(cycles) == 0: 
        # Check Connected
        # From CDG_Vertexs, CDG_Edges to Connectivity

        Connected_list = []
        # Check Connectivity of X to Brs
        checkingList = []
        reachableList = []
        for br in brs:
            checkingList.append("X_N"+str(br))
        new_network.DFS(checkingList, reachableList)
        Connected_list.append(new_network.isConnected(reachableList, "X"))

        # Check Connectivity of brs to X
        for br in brs:
            checkingList = new_network.get_Neighbor("N"+str(br))
            reachableList = []
            new_network.DFS(checkingList, reachableList)
            Connected_list.append(new_network.isConnected(reachableList, "N"+str(br)))

        if all(Connected_list):
            # Evaluate Placement and Turn Restriction
            cur_eva = new_network.evaluate(abstract_node, brs)

            global min_eva
            if cur_eva > min_eva:
                print("Not Minimal Eva")
                return

            print("Restricted Turn")
            for turn_restrict in pt:
                print(turn_restrict[0].name, turn_restrict[1].name)

            min_eva = cur_eva
            print("Current Eva", min_eva)

            #print("Valid Turn")
            #for turn_restrict in new_network.cdg_edges:
            #    print(turn_restrict[0], turn_restrict[1])

            # We believe the less pt the better
            min_tr = len(pt)

            #print("Turn Res")
            #for turn_restrict in pt:
            #    print(turn_restrict[0].name, turn_restrict[1].name)
            return
        else: # Not connected, return
            #print("Not Connected", len(pt))
            return
    else: # Has Cycle, Setrurn
        #print("Has Cycle", len(pt))

        for i in range(start, end):
            pt.append(bt[i])
            setTurn(network, abstract_node, brs, bt, pt, i+1, end)
            pt.pop()

# Generate Basic Network
topo = Mesh(n_nodes=16, n_cols=4, n_rows=4)
routing = XYRouting()
network = Network(topo, routing)

abstract_node = RouterNode("X", 16)
#abstract_node = RouterNode("X", 9)

#br_lists = [2, 11, 13]
br_lists = [1, 2, 13, 14]


for br0 in range(len(br_lists)):
    for br1 in range(br0+1, len(br_lists)):
        for br2 in range(br1+1, len(br_lists)):
            for br3 in range(br2+1, len(br_lists)):

                # Boundary Router Placement
                cur_brs = [br_lists[br0], br_lists[br1], br_lists[br2], br_lists[br3]]
                #cur_brs = [br_lists[br0], br_lists[br1], br_lists[br2]]
                cur_network = copy.deepcopy(network)
                print("Current BR: ", cur_brs)

                # Add Links to current BR placement 
                new_link_lists = []
                for br in cur_brs:
                    new_links = cur_network.topology.add_link(abstract_node, network.topology.nodes[br])
                    new_link_lists.append(new_links[0])
                    new_link_lists.append(new_links[1])
                cur_network.gen_cdg(abstract_node)

                turn_restriction_lists = []

                # Generate turn restriction
                for head_link in new_link_lists:
                    for tail_link in network.topology.links:
                        head_link_head = network.get_Node(head_link,abstract_node)[0]
                        head_link_tail = network.get_Node(head_link,abstract_node)[1]
                        tail_link_head = network.get_Node(tail_link,abstract_node)[0]
                        tail_link_tail = network.get_Node(tail_link,abstract_node)[1]

                        if head_link_tail == tail_link_head and head_link_head != tail_link_tail:
                            turn_restriction_lists.append([head_link, tail_link])

                for tail_link in new_link_lists:
                    for head_link in network.topology.links:
                        head_link_head = network.get_Node(head_link,abstract_node)[0]
                        head_link_tail = network.get_Node(head_link,abstract_node)[1]
                        tail_link_head = network.get_Node(tail_link,abstract_node)[0]
                        tail_link_tail = network.get_Node(tail_link,abstract_node)[1]

                        if head_link_tail == tail_link_head and head_link_head != tail_link_tail:
                            turn_restriction_lists.append([head_link, tail_link])

                # Search for best turn restriction
                b_turn = turn_restriction_lists
                p_turn = []
                setTurn(cur_network, abstract_node, cur_brs, b_turn, p_turn, 0, len(b_turn)-1)




