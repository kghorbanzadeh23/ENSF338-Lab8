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
        if n1 in self.adjacency_list and n2 in self.adjacency_list:
            self.adjacency_list[n1].append((n2, weight))
            self.adjacency_list[n2].append((n1, weight))

    def removeEdge(self, n1, n2):
        if n1 in self.adjacency_list and n2 in self.adjacency_list:
            self.adjacency_list[n1] = [(node, weight) for node, weight in self.adjacency_list[n1] if node != n2]
            self.adjacency_list[n2] = [(node, weight) for node, weight in self.adjacency_list[n2] if node != n1]

    def importFromFile(self, file):
        self.adjacency_list = {}
        self.nodeList = []
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
                            n1 = self.addNode(int( nodes[0]))
                            n2 = self.addNode(int((nodes[1])[0:-13]))
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
            return self.nodeList

        except FileNotFoundError:
            print("File not found.")
            return None



# Testing the Graph class

# Create a new graph
graph = Graph()


node1 = graph.addNode("node1")
node2 = graph.addNode("node2")
node3 = graph.addNode("node3")
node4 = graph.addNode("node4")

# Add edges
graph.addEdge(node1, node2, 5)
graph.addEdge(node2, node3)
graph.addEdge(node4, node3, 6)

# Remove an edge
graph.removeEdge(node1, node2)

# Import from file
imported_graph = Graph()
imported_graph.importFromFile("random.dot")

# Print the adjacency list
print("Original Graph:")
print(graph.adjacency_list)

print("\nImported Graph:")
print(imported_graph.adjacency_list if imported_graph else "Graph import failed.")
