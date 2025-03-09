from collections import deque, defaultdict

def build_graph(num_nodes, edges):
	"""Build an undirected tree graph from given num of nodes and edges."""

	graph = defaultdict(list)
	for u, v in edges:
		graph[u].append(v)
		graph[v].append(u)
	return graph

def bfs_distances(graph, start):
	""""""
	distances = {start: 0}
	queue = deque([start])
	
	while queue:
		vertex = queue.popleft()
		for neighbor in graph[vertex]:
			if neighbor not in distances:
				distances[neighbor] = distances[vertex] + 1
				queue.append(neighbor)
	return distances

# Example undirected tree
num_nodes = 4
edges = [
	(1, 2),
	(1, 3),
	(3, 4)
]

graph = build_graph(num_nodes, edges)
print(graph)
distances = bfs_distances(graph, 1)

# Print distances in order of node number
for node in sorted(distances):
	print(f"Node {node}: Distance = {distances[node]}")
