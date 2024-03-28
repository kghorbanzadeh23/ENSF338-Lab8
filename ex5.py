# Topological sorting can be implemented using Depth-First Search (DFS).
# Finding Cycles: Only Directed Acyclic Graphs (DAGs) allow for topological
# sorting. A graph's cycles may be found using DFS, which is important because
# a topological sort cannot be completed in the presence of a cycle.

# Ordering: Before turning around, DFS travels as far as feasible down each branch.
# This parameter makes sure that all outgoing edges from a node are visited before the
# node is closed, meaning that all descendants of a given node are visited before the node
# is finished. This is a useful characteristic since a node in a topological sort has to come
# after all of its dependencies, or graph descendants.

# Stack Usage: To preserve the vertex order in a DFS implementation for topological sorting,
# a stack is usually employed. A vertex is pushed into the stack each time it is completed,
# meaning that all of its edges have been investigated. The stack has a legitimate topological
# ordering from the bottom to the top once every vertex has been visited.

class GraphNode:
    def __init__(self, data):
        self.data = data
        self.indegree = 0

    def __repr__(self):
        return f'{self.data}'

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
            n2.indegree += 1

    def removeEdge(self, n1, n2):
        if n1 in self.adjacency_list and n2 in self.adjacency_list:
            self.adjacency_list[n1] = [(node, weight) for node, weight in self.adjacency_list[n1] if node != n2]
            if (n2, weight) in self.adjacency_list[n1]:
                n2.indegree -= 1

    def isdag(self):
        def _dfs(node, visited, recStack):
            visited[node] = True
            recStack[node] = True
            for neighbour, _ in self.adjacency_list[node]:
                if not visited[neighbour]:
                    if _dfs(neighbour, visited, recStack):
                        return True
                elif recStack[neighbour]:
                    return True
            recStack[node] = False
            return False

        visited = {node: False for node in self.adjacency_list}
        recStack = {node: False for node in self.adjacency_list}
        for node in self.adjacency_list:
            if not visited[node]:
                if _dfs(node, visited, recStack):
                    return False
        return True

    def toposort(self):
        if not self.isdag():
            return None

        topo_order = []
        zero_indegree_queue = [node for node in self.adjacency_list if node.indegree == 0]

        while zero_indegree_queue:
            node = zero_indegree_queue.pop(0)
            topo_order.append(node)

            for neighbour, _ in self.adjacency_list[node]:
                neighbour.indegree -= 1
                if neighbour.indegree == 0:
                    zero_indegree_queue.append(neighbour)

        if len(topo_order) == len(self.adjacency_list):
            return topo_order
        else:
            return None

# Scenario 1: Graph with a cycle
graph_with_cycle = Graph()
node_1 = graph_with_cycle.addNode('1')
node_2 = graph_with_cycle.addNode('2')
node_3 = graph_with_cycle.addNode('3')
graph_with_cycle.addEdge(node_1, node_2)
graph_with_cycle.addEdge(node_2, node_3)
graph_with_cycle.addEdge(node_3, node_1)

# Scenario 2: Graph without a cycle
graph_without_cycle = Graph()
node_a = graph_without_cycle.addNode('A')
node_b = graph_without_cycle.addNode('B')
node_c = graph_without_cycle.addNode('C')
node_d = graph_without_cycle.addNode('D')
graph_without_cycle.addEdge(node_a, node_b)
graph_without_cycle.addEdge(node_a, node_c)
graph_without_cycle.addEdge(node_b, node_d)
graph_without_cycle.addEdge(node_c, node_d)

# Testing isdag on both graphs
isdag_with_cycle_result = graph_with_cycle.isdag()
isdag_without_cycle_result = graph_without_cycle.isdag()

# Testing topsort on both graphs
topsort_with_cycle_result = graph_with_cycle.toposort()
topsort_without_cycle_result = graph_without_cycle.toposort()

print(f'Graph with cycle is a DAG: {isdag_with_cycle_result}')
print(f'Topological Sort (Graph with cycle): {topsort_with_cycle_result}')

print(f'Graph without cycle is a DAG: {isdag_without_cycle_result}')
print(f'Topological Sort (Graph without cycle): {topsort_without_cycle_result}')