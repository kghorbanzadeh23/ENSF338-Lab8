import heapq
import time
import statistics
import matplotlib.pyplot as plt

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

# the slower implementation would be an unsorted Array or List
class Node:
    def __init__(self, vertex, dist):
        self.vertex = vertex
        self.dist = dist

class UnsortedArrayQueue:
    def __init__(self):
        self.nodes = []
    
    def insert(self, node):
        self.nodes.append(node)
    
    def extract_min(self):
        min_node = min(self.nodes, key=lambda node: node.dist)
        self.nodes.remove(min_node)
        return min_node

# the faster implementation would be a min-heap/priority queue

class MinHeapQueue:
    def __init__(self):
        self.heap = []
    
    def insert(self, node):
        heapq.heappush(self.heap, (node.dist, node))
    
    def extract_min(self):
        return heapq.heappop(self.heap)[1]
    
class Graph(Graph):
    # Using Dijkstra's Algorithm with an Unsorted Array
    def slowSP(self, start_node):
        distances = {node: float('infinity') for node in self.adjacency_list}
        distances[start_node] = 0
        
        queue = UnsortedArrayQueue()
        queue.insert(Node(start_node, 0))

        while queue.nodes:
            current_node = queue.extract_min().vertex
            for neighbor, weight in self.adjacency_list[current_node]:
                distance = distances[current_node] + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    queue.insert(Node(neighbor, distance))

        return distances

    # Using Dijkstra's Algorithm with a Min-Heap
    def fastSP(self, start_node):
        distances = {node: float('infinity') for node in self.adjacency_list}
        distances[start_node] = 0
        
        queue = MinHeapQueue()
        queue.insert(Node(start_node, 0))

        while queue.heap:
            current_node = queue.extract_min().vertex
            for neighbor, weight in self.adjacency_list[current_node]:
                distance = distances[current_node] + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    queue.insert(Node(neighbor, distance))

        return distances
    
# Initialize the graph
graph = Graph()

# Assume that the file 'random.dot' is in the current working directory
graph.importFromFile('random.dot')

# Performance measurement for slowSP
slow_times = []
for node in graph.adjacency_list.keys():
    start_time = time.time()
    graph.slowSP(node)
    end_time = time.time()
    slow_times.append(end_time - start_time)

# Performance measurement for fastSP
fast_times = []
for node in graph.adjacency_list.keys():
    start_time = time.time()
    graph.fastSP(node)
    end_time = time.time()
    fast_times.append(end_time - start_time)

# Calculate and print the performance metrics for slowSP
slow_average_time = statistics.mean(slow_times)
slow_max_time = max(slow_times)
slow_min_time = min(slow_times)

print(f"SlowSP - Average Time: {slow_average_time}")
print(f"SlowSP - Max Time: {slow_max_time}")
print(f"SlowSP - Min Time: {slow_min_time}")

# Calculate and print the performance metrics for fastSP
fast_average_time = statistics.mean(fast_times)
fast_max_time = max(fast_times)
fast_min_time = min(fast_times)

print(f"FastSP - Average Time: {fast_average_time}")
print(f"FastSP - Max Time: {fast_max_time}")
print(f"FastSP - Min Time: {fast_min_time}")

# Plot histogram for slowSP execution times
plt.hist(slow_times, bins=20, alpha=0.5, label='slowSP')

# Plot histogram for fastSP execution times
plt.hist(fast_times, bins=20, alpha=0.5, label='fastSP')

plt.xlabel('Execution Time (seconds)')
plt.ylabel('Frequency')
plt.title('Histogram of Execution Times for slowSP and fastSP')
plt.legend(loc='upper right')

plt.savefig('ex2.jpeg')

"""
Discussion of Results:
The slowSP method uses an unsorted array and should typically show a wider distribution with a higher average
execution time due to its inefficient node selection logic.The fastSP method uses a min-heap and should have a
narrower distribution with a lower average execution time, reflecting its more efficient node selection logic.
The histograms will allow you to visualize the spread and central tendency of the execution times for both
methods. The comparison between the two histograms will highlight the performance difference, with fastSP
expected to be clustered towards lower execution times.
"""
