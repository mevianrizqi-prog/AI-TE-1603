"""Algoritma pencarian rute ke pintu keluar terdekat.

Semua algoritma menerima: graf, titik awal, dan himpunan node terblokir (bahaya).
Tujuan = pintu keluar mana pun yang tidak terblokir.
"""
import heapq
from collections import deque
from dataclasses import dataclass
from itertools import count
from typing import List, Optional

from .graph import BuildingGraph


@dataclass
class SearchResult:
    algorithm: str
    path: Optional[List[str]]   # None jika tidak ada jalur
    distance: Optional[float]   # meter
    hops: Optional[int]         # jumlah langkah antar node
    expanded: int               # jumlah node yang diekspansi

    @property
    def found(self) -> bool:
        return self.path is not None


def _build_path(parent, node):
    path = [node]
    while parent[path[-1]] is not None:
        path.append(parent[path[-1]])
    return path[::-1]


def _result(name, graph, parent, node, expanded):
    path = _build_path(parent, node)
    return SearchResult(name, path, graph.path_distance(path), len(path) - 1, expanded)


def _none(name, expanded):
    return SearchResult(name, None, None, None, expanded)


def bfs(graph: BuildingGraph, start: str, blocked=()) -> SearchResult:
    """Breadth-First Search: rute dengan jumlah langkah paling sedikit."""
    goals = graph.exits(blocked)
    frontier = deque([start])
    parent = {start: None}
    expanded = 0
    while frontier:
        node = frontier.popleft()
        expanded += 1
        if node in goals:
            return _result("BFS", graph, parent, node, expanded)
        for nxt, _ in graph.neighbors(node, blocked):
            if nxt not in parent:
                parent[nxt] = node
                frontier.append(nxt)
    return _none("BFS", expanded)


def ucs(graph: BuildingGraph, start: str, blocked=()) -> SearchResult:
    """Uniform-Cost Search: rute dengan jarak (meter) terpendek."""
    goals = graph.exits(blocked)
    tie = count()
    frontier = [(0.0, next(tie), start)]
    parent = {start: None}
    best = {start: 0.0}
    done = set()
    expanded = 0
    while frontier:
        g, _, node = heapq.heappop(frontier)
        if node in done:
            continue
        done.add(node)
        expanded += 1
        if node in goals:
            return _result("UCS", graph, parent, node, expanded)
        for nxt, w in graph.neighbors(node, blocked):
            ng = g + w
            if nxt not in best or ng < best[nxt]:
                best[nxt] = ng
                parent[nxt] = node
                heapq.heappush(frontier, (ng, next(tie), nxt))
    return _none("UCS", expanded)


def astar(graph: BuildingGraph, start: str, blocked=()) -> SearchResult:
    """A*: seperti UCS, tapi dipandu heuristik jarak garis lurus ke pintu keluar."""
    goals = graph.exits(blocked)
    if not goals:
        return _none("A*", 0)
    tie = count()
    frontier = [(graph.heuristic(start, goals), next(tie), 0.0, start)]
    parent = {start: None}
    best = {start: 0.0}
    done = set()
    expanded = 0
    while frontier:
        _, _, g, node = heapq.heappop(frontier)
        if node in done:
            continue
        done.add(node)
        expanded += 1
        if node in goals:
            return _result("A*", graph, parent, node, expanded)
        for nxt, w in graph.neighbors(node, blocked):
            ng = g + w
            if nxt not in best or ng < best[nxt]:
                best[nxt] = ng
                parent[nxt] = node
                heapq.heappush(frontier, (ng + graph.heuristic(nxt, goals), next(tie), ng, nxt))
    return _none("A*", expanded)


def reachable_exits(graph: BuildingGraph, start: str, blocked=()) -> int:
    """Hitung berapa pintu keluar (tidak terblokir) yang masih bisa dicapai dari start."""
    goals = graph.exits(blocked)
    seen = {start}
    stack = [start]
    while stack:
        node = stack.pop()
        for nxt, _ in graph.neighbors(node, blocked):
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return len(seen & goals)


ALGORITHMS = {"BFS": bfs, "UCS": ucs, "A*": astar}
