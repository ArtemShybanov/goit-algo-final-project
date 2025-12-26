from __future__ import annotations

from dataclasses import dataclass # to automatically generate __init__ and __repr__ methods for edge representing
from heapq import heappop, heappush
from typing import Any


@dataclass(frozen=True) # frozen=True to create immutable object
class Edge:
    to: Any
    weight: float


class WeightedGraph:
    def __init__(self) -> None:
        # List of outgoing edges
        self._adj = {}

    def add_node(self, node: Any) -> None:
        # Ensure node exists in the list
        self._adj.setdefault(node, [])

    def add_edge(self, u: Any, v: Any, w: float, *, undirected: bool = False) -> None:
        # Add a weighted edge
        if w < 0:
            raise ValueError("Dijkstra requires non-negative edge weights.")

        self.add_node(u)
        self.add_node(v)

        self._adj[u].append(Edge(v, w))
        if undirected:
            self._adj[v].append(Edge(u, w))

    def neighbors(self, node: Any) -> list[Edge]:
        # Return outgoing edges for node
        return self._adj.get(node, [])

    def nodes(self) -> list[Any]:
        # Return all nodes in the graph
        return list(self._adj.keys())

# Dijkstra shortest paths using a binary heap (heapq)
def dijkstra(graph: WeightedGraph, start: Any) -> tuple[dict[Any, float], dict[Any, Any | None]]:
    if start not in graph.nodes():
        graph.add_node(start)

    dist = {node: float("inf") for node in graph.nodes()}
    prev = {node: None for node in graph.nodes()}

    dist[start] = 0.0

    # Min-heap stores (distance_so_far, node)
    heap = [(0.0, start)]

    while heap:
        cur_dist, u = heappop(heap)

        # Skip stale heap entries
        if cur_dist != dist[u]:
            continue

        # Relax edges
        for e in graph.neighbors(u):
            v = e.to
            alt = cur_dist + e.weight

            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                heappush(heap, (alt, v))

    return dist, prev


def reconstruct_path(prev: dict[Any, Any | None], start: Any, target: Any) -> list[Any]:
    # Reconstruct path start -target using predecessor links
    if start == target:
        return [start]

    path = []
    cur = target

    while cur is not None:
        path.append(cur)
        if cur == start:
            break
        cur = prev.get(cur)

    if not path or path[-1] != start:
        return [] # no path

    path.reverse()
    return path


if __name__ == "__main__":
    # Test graph
    g = WeightedGraph()
    g.add_edge("A", "B", 4, undirected=True)
    g.add_edge("A", "C", 2, undirected=True)
    g.add_edge("B", "C", 1, undirected=True)
    g.add_edge("B", "D", 5, undirected=True)
    g.add_edge("C", "D", 8, undirected=True)
    g.add_edge("C", "E", 10, undirected=True)
    g.add_edge("D", "E", 2, undirected=True)
    g.add_edge("D", "F", 6, undirected=True)
    g.add_edge("E", "F", 3, undirected=True)

    start_node = "A"
    dist, prev = dijkstra(g, start_node)

    print(f"Start: {start_node}\n")
    for node in sorted(g.nodes()):
        d = dist[node]
        if d == float("inf"):
            print(f"{node}: unreachable")
            continue

        path = reconstruct_path(prev, start_node, node)
        path_str = " -> ".join(map(str, path))
        print(f"{node}: shortest_distance={d:.0f}, path={path_str}")