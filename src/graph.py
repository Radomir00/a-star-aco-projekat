import json


class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []

    def add_edge(self, node_a, node_b, weight):
        self.add_node(node_a)
        self.add_node(node_b)
        self.graph[node_a].append((node_b, weight))
        self.graph[node_b].append((node_a, weight))

    def neighbors(self, node):
        return self.graph.get(node, [])

    def weight(self, node_a, node_b):
        for neighbor, w in self.graph.get(node_a, []):
            if neighbor == node_b:
                return w
        return None

    def nodes(self):
        return list(self.graph.keys())

    def has_edge(self, node_a, node_b):
        return any(neighbor == node_b for neighbor, _ in self.graph.get(node_a, []))

    def __len__(self):
        return len(self.graph)

    def __repr__(self):
        return f"Graph(nodes={len(self.graph)})"


def load_graph_from_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    graph = Graph()
    for node, neighbors in data.items():
        graph.add_node(node)
        graph.graph[node] = [(neighbor, weight) for neighbor, weight in neighbors]

    return graph


if __name__ == "__main__":
    g = load_graph_from_json("data/bih.json")

    print("Broj cvorova:", len(g))
    print("Susjedi od Banja Luka:", g.neighbors("Banja Luka"))
    print("Tezina Banja Luka - Prnjavor:", g.weight("Banja Luka", "Prnjavor"))
