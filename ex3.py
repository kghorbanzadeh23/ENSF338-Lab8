class GraphNode:
    def __init__(self, data):
        self.data = data


class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def addNode(self, data):
        node = GraphNode(data)
        self.adjacency_list[node] = []
        return node

    def removeNode(self, node):
        if node in self.adjacency_list:
            del self.adjacency_list[node]
            for key in self.adjacency_list:
                self.adjacency_list[key] = [n for n in self.adjacency_list[key] if n != node]

    def addEdge(self, n1, n2, weight=1):
        if n1 in self.adjacency_list and n2 in self.adjacency_list:
            self.adjacency_list[n1].append((n2, weight))
            self.adjacency_list[n2].append((n1, weight))

    def removeEdge(self, n1, n2):
        if n1 in self.adjacency_list and n2 in self.adjacency_list:
            self.adjacency_list[n1] = [(node, weight) for node, weight in self.adjacency_list[n1] if node != n2]
            self.adjacency_list[n2] = [(node, weight) for node, weight in self.adjacency_list[n2] if node != n1]

    def importFromFile(self, file):
        self.adjacency_list = {}

        try:
            with open(file, 'r') as f:
                lines = f.readlines()

            # Check if the file starts with the expected format
            if len(lines) < 2 or not lines[0].startswith("strict graph"):
                print("Invalid GraphViz file format.")
                return None

            # Parse the lines to extract nodes and edges
            for line in lines[1:]:
                line = line.strip()
                if line and line[0] != '}':
                    if "[" in line and "]" in line:
                        # If weight is specified
                        parts = line.split('--')
                        if len(parts) == 2:
                            nodes = [n.strip() for n in parts]
                            weight = int(line.split('weight=')[1].split(']')[0].strip())
                            n1 = self.addNode(nodes[0])
                            n2 = self.addNode(nodes[1])
                            self.addEdge(n1, n2, weight)
                    else:
                        # If weight is not specified (implicitly 1)
                        parts = line.split('--')
                        if len(parts) == 2:
                            nodes = [n.strip() for n in parts]
                            n1 = self.addNode(nodes[0])
                            n2 = self.addNode(nodes[1])
                            self.addEdge(n1, n2)

            print("Graph imported successfully.")
            return self

        except FileNotFoundError:
            print("File not found.")
            return None

    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def apply_union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    def kruskal_algo(self):
        result = []
        i, e = 0, 0
        self.adjacency_list = sorted(self.adjacency_list, key=lambda item: item[2])
        parent = []
        rank = []
        for node in range(self.V):
            parent.append(node)
            rank.append(0)
        while e < self.V - 1:
            u, v, w = self.adjacency_list[i]
            i = i + 1
            x = self.find(parent, u)
            y = self.find(parent, v)
            if x != y:
                e = e + 1
                result.append([u, v, w])
                self.apply_union(parent, rank, x, y)
        for u, v, weight in result:
            print("%d - %d: %d" % (u, v, weight))