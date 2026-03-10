graph = {
    'A': ['B', 'D'],
    'B': ['A', 'C'],
    'C': ['B'],
    'D': ['A']
}

def bfs(graph, start):
    visited = set()
    queue = [start]

    order = []
    distance = {start: 0}

    while queue:
        current = queue.pop(0)
        if current not in visited:
            visited.add(current)
            order.append(current)

            for neighbor in graph[current]:
                if neighbor not in visited:
                    queue.append(neighbor)

                    distance[neighbor] = distance[current] + 1

                    return order, distance

print(bfs(graph, 'A'))