"""Model gedung sebagai graf: ruangan = node, jalur antar ruangan = edge."""
import json
import math
from dataclasses import dataclass
from typing import Dict, Iterable, List, Set, Tuple

STAIR_PENALTY = 8.0  # tambahan jarak (meter) saat pindah lantai lewat tangga


@dataclass(frozen=True)
class Node:
    id: str
    name: str
    floor: int
    x: float
    y: float
    is_exit: bool = False


class BuildingGraph:
    def __init__(self, nodes: List[Node], edges: List[Tuple[str, str]]):
        self.nodes: Dict[str, Node] = {n.id: n for n in nodes}
        self.adj: Dict[str, Dict[str, float]] = {n.id: {} for n in nodes}
        for a, b in edges:
            if a not in self.nodes or b not in self.nodes:
                raise ValueError(f"Edge tidak valid: {a} - {b}")
            w = self._weight(self.nodes[a], self.nodes[b])
            self.adj[a][b] = w
            self.adj[b][a] = w

    @staticmethod
    def _weight(a: Node, b: Node) -> float:
        d = math.hypot(a.x - b.x, a.y - b.y)
        if a.floor != b.floor:
            d += STAIR_PENALTY
        return round(d, 1)

    @classmethod
    def from_json(cls, path: str) -> "BuildingGraph":
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        nodes = [Node(n["id"], n["name"], n["floor"], n["x"], n["y"], n.get("exit", False))
                 for n in data["nodes"]]
        return cls(nodes, [tuple(e) for e in data["edges"]])

    def neighbors(self, node_id: str, blocked: Iterable[str] = ()):
        """Tetangga yang tidak terblokir, beserta jarak (meter)."""
        blocked = set(blocked)
        return [(n, w) for n, w in self.adj[node_id].items() if n not in blocked]

    def exits(self, blocked: Iterable[str] = ()) -> Set[str]:
        blocked = set(blocked)
        return {i for i, n in self.nodes.items() if n.is_exit and i not in blocked}

    def heuristic(self, node_id: str, goals: Set[str]) -> float:
        """Jarak garis lurus (denah) ke pintu keluar terdekat. Tidak pernah melebihi jarak sebenarnya."""
        a = self.nodes[node_id]
        return min(math.hypot(a.x - self.nodes[g].x, a.y - self.nodes[g].y) for g in goals)

    def path_distance(self, path: List[str]) -> float:
        return round(sum(self.adj[a][b] for a, b in zip(path, path[1:])), 1)
