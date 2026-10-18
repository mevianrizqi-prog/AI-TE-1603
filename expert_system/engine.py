from dataclasses import dataclass
from typing import List, Optional

from search_algorithm import ALGORITHMS, BuildingGraph, SearchResult, reachable_exits
from .rules import RULES, STATUS, Facts


@dataclass
class Diagnosis:
    status: str
    result: SearchResult
    messages: List[str]
    fired_rules: List[str]
    path_names: List[str]


def diagnose(graph: BuildingGraph, start: str, blocked=(), algorithm: str = "BFS") -> Diagnosis:
    if start not in graph.nodes:
        raise KeyError(f"Lokasi tidak dikenal: {start}")
    if algorithm not in ALGORITHMS:
        raise KeyError(f"Algoritma tidak dikenal: {algorithm}")
    blocked = frozenset(blocked)
    search = ALGORITHMS[algorithm]

    result = search(graph, start, blocked)
    baseline = search(graph, start, ())
    facts = Facts(graph, start, blocked, result, baseline, reachable_exits(graph, start, blocked))

    fired = [r for r in RULES if r.condition(facts)]
    level = max((r.level for r in fired), default=0)
    names = [graph.nodes[n].name for n in (result.path or [])]
    return Diagnosis(STATUS[level], result, [r.message(facts) for r in fired],
                     [r.id for r in fired], names)
