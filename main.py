import networkx as nx
import copy
import itertools
from tqdm import tqdm
from graphviz import Graph, Digraph
from Topology import Topology, Mesh
from Router import RouterNode, Link, XYRouting
from Network import Network

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

# Generate Basic Network
topo = Mesh(n_nodes=16, n_cols=4, n_rows=4)
#topo = Mesh(n_nodes=9, n_cols=3, n_rows=3)
routing = XYRouting()
network = Network(topo, routing)

#abstract_node = RouterNode("X", 16)
abstract_node = RouterNode("X", 9)

br_lists = [0, 1, 2, 3, 4, 7, 8, 11, 12, 13, 14, 15]
#br_lists = [0, 1, 2, 3, 5, 6, 7, 8]

for br0 in range(len(br_lists)):
    for br1 in range(br0+1, len(br_lists)):
        for br2 in range(br1+1, len(br_lists)):
            for br3 in range(br2+1, len(br_lists)):

                # Boundary Router Placement
                cur_brs = [br_lists[br0], br_lists[br1], br_lists[br2], br_lists[br3]]
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
                
                # Iterate all turn restriction selecion
                all_combinations = []
                for r in range(1, len(turn_restriction_lists) + 1):
                    combination = list(itertools.combinations(turn_restriction_lists, r))
                    all_combinations.extend(combination)

                for TR in tqdm(all_combinations, desc="Processing"):
                    # rebuild cdg
                    final_network= copy.deepcopy(cur_network)
                    final_network.gen_cdg(abstract_node, TR)

                    # Check Cycle
                    G = nx.DiGraph()
                    G.add_nodes_from(final_network.cdg_vertexs)
                    G.add_edges_from(final_network.cdg_edges)
                    if len(list(nx.simple_cycles(G))) != 0:
                        continue

                    # Check Connected
                    if not nx.is_strongly_connected(G):
                        continue

                    # Evaluate Placement and Turn Restriction
                    cur_eva = final_network.evaluate()

                    print(cur_brs)
                    for turn_restrict in TR:
                        print(turn_restrict[0].name, turn_restrict[1].name)
                    




