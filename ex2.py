import heapq

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
