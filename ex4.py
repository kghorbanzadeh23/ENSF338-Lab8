import timeit
import random
import sys

sys.setrecursionlimit(5000)
class GraphNode:
    def __init__(self, data):
        self.data = data
    def equals(self, node):
        if(node.data == self.data):
            return True
        return False
class Graph2:
    def __init__(self):
        self.adjacency_matrix = {}
        self.nodeList = []

    def addNode(self, data):
        node = GraphNode(data)
        for nodeOb in self.nodeList:
            if node.equals(nodeOb):
                return nodeOb
            
        self.nodeList.append(node)
        if node.data not in self.adjacency_matrix:
            self.adjacency_matrix[node] = {}
            for existing_node in self.adjacency_matrix:
                self.adjacency_matrix[existing_node][node] = 0
            self.adjacency_matrix[node][node] = 0  # diagonal element
        return node

    def removeNode(self, node):
        if node.data in self.adjacency_matrix:
            del self.adjacency_matrix[node.data]
            for key in self.adjacency_matrix:
                del self.adjacency_matrix[key][node.data]

    def addEdge(self, n1, n2, weight=1):
        if n1 in self.adjacency_matrix and n2 in self.adjacency_matrix:
            self.adjacency_matrix[n1][n2] = weight
            self.adjacency_matrix[n2][n1] = weight

    def removeEdge(self, n1, n2):
        if n1.data in self.adjacency_matrix and n2.data in self.adjacency_matrix:
            self.adjacency_matrix[n1.data][n2.data] = 0
            self.adjacency_matrix[n2.data][n1.data] = 0

    def importFromFile(self, file):
        self.adjacency_matrix = {}
        nodes = []
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
            return nodes

        except FileNotFoundError:
            print("File not found.")
            return None
        
    def dfs(self, start_node):
        visited = []
        result = []

        def dfs_recursive(node):
            visited.append(node)
            result.append(node)
            for neighbor, weight in self.adjacency_matrix[node].items():
                for nodeOb in visited:
                    if nodeOb.equals(node):
                        return           
                if weight != 0:         
                    dfs_recursive(neighbor)

        dfs_recursive(start_node)
        return result
    
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

    def dfs_recursive(self, node, visited, result):
        visited.append(node)
        result.append(node)
        for neighbor, _ in self.adjacency_list[node]:  # Fixed iteration over adjacency list
            for nodeOb in visited:
                if nodeOb.equals(node):
                    return
            self.dfs_recursive(neighbor, visited, result)

    def dfs(self, start_node):
        visited = []
        result = []

        self.dfs_recursive(start_node, visited, result)
        return result
    
def measureTimes(graph):
    graph.importFromFile("random.dot")
    print(len(graph.nodeList))
    times = timeit.repeat(lambda: graph.dfs(graph.nodeList[0]), repeat=10)

    return times

graph = Graph()
graphOneTimes = measureTimes(graph)

print("Graph one times - Max:", max(graphOneTimes), "Min:", min(graphOneTimes), "Avg:", sum(graphOneTimes)/len(graphOneTimes))

graph = Graph2()
graphTwoTimes = measureTimes(graph)


print("Graph one times - Max:", max(graphTwoTimes), "Min:", min(graphTwoTimes), "Avg:", sum(graphTwoTimes)/len(graphTwoTimes))