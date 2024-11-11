from Router import RouterNode, Link

class Topology(object):
    n_nodes = 0
    nodes = []
    links = []
    topo_type = None
    routing_alg = None

    def __init__(self, n_nodes) -> None:
        self.n_nodes = n_nodes
        nodes = []
        links = []


class Mesh(Topology):
    n_cols = 4;
    n_rows = 4;

    def __init__(self, n_nodes, n_cols, n_rows):
        super().__init__(n_nodes)
        n_cols = n_cols
        n_rows = n_rows
        self.gen_nodes()
        self.gen_links()

    def gen_nodes(self):
        for i in range(self.n_nodes):
            node = RouterNode("N"+str(i), i)
            self.nodes.append(node)

    def gen_links(self):
        for i in range(self.n_cols):
            for j in range(self.n_rows):
                current_node = self.nodes[i * self.n_cols + j]
                if j >= 0 and j < self.n_cols - 1:
                    link = Link(current_node, self.nodes[i * self.n_cols + j + 1])
                    self.links.append(link)
                if i >= 0 and i < self.n_rows - 1:
                    link = Link(current_node, self.nodes[(i + 1) * self.n_cols + j])
                    self.links.append(link)
                if j >= 1 and j < self.n_cols:
                    link = Link(current_node, self.nodes[i * self.n_cols + j - 1])
                    self.links.append(link)
                if i >= 1 and i < self.n_rows:
                    link = Link(current_node, self.nodes[(i - 1) * self.n_cols + j])
                    self.links.append(link)





