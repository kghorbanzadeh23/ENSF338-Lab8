
class GraphNode:
    def __init__(self, data):
        self.data = data

    def equals(self, node):
        if(node.data == self.data):
            return True
        return False

class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.nodeList = []

    def addNode(self, data):
        node = GraphNode(data)
        for nodeOb in self.nodeList:
            if node.equals(nodeOb):
                return nodeOb

        self.adjacency_list[node] = []
        self.nodeList.append(node)
        return node

    def removeNode(self, node):
        if node in self.adjacency_list:
            del self.adjacency_list[node]
            for key in self.adjacency_list:
                self.adjacency_list[key] = [n for n in self.adjacency_list[key] if n != node]

    def addEdge(self, n1, n2, weight=1):
        for nodeOb in self.nodeList:
            if n1.equals(nodeOb):
                n1 = nodeOb
            if n2.equals(nodeOb):
                n2 = nodeOb

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

    def find(self, parent, node):
        if parent[node] == node:
            return node
        return self.find(parent, parent[node])

    def union(self, parent, rank, node1, node2):
        root1 = self.find(parent, node1)
        root2 = self.find(parent, node2)

        if rank[root1] < rank[root2]:
            parent[root1] = root2
        elif rank[root1] > rank[root2]:
            parent[root2] = root1
        else:
            parent[root2] = root1
            rank[root1] += 1

    def mst(self):
        parent = {}
        rank = {}
        result = Graph()

        for node in self.adjacency_list:
            parent[node] = node
            rank[node] = 0

        edges = []
        for node in self.adjacency_list:
            for neighbor, weight in self.adjacency_list[node]:
                edges.append((weight, node, neighbor))

        edges.sort(key=lambda x: x[0])

        for edge in edges:
            weight, node1, node2 = edge
            root1 = self.find(parent, node1)
            root2 = self.find(parent, node2)

            if root1 != root2:
                result.addNode(node1.data)
                result.addNode(node2.data)
                result.addEdge(node1, node2, weight)
                self.union(parent, rank, root1, root2)

        return result

# Create a graph
g = Graph()

# Add nodes
nodes = {}
nodes['A'] = g.addNode('A')
nodes['B'] = g.addNode('B')
nodes['C'] = g.addNode('C')
nodes['D'] = g.addNode('D')
nodes['E'] = g.addNode('E')

# Add edges
g.addEdge(nodes['A'], nodes['B'], 4)
g.addEdge(nodes['A'], nodes['C'], 2)
g.addEdge(nodes['A'], nodes['D'], 5)
g.addEdge(nodes['B'], nodes['D'], 6)
g.addEdge(nodes['B'], nodes['E'], 3)
g.addEdge(nodes['C'], nodes['D'], 1)
g.addEdge(nodes['D'], nodes['E'], 7)

# Find minimum spanning tree
mst = g.mst()

# Print the edges of the minimum spanning tree
for node in mst.adjacency_list:
    print(len(mst.adjacency_list[node]))
