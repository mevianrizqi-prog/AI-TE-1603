"""Basis aturan (rule-based expert system) untuk menafsirkan hasil pencarian rute.

Setiap aturan: JIKA <kondisi pada fakta> MAKA <tingkat status + pesan/saran>.
Tingkat status: 0 = AMAN, 1 = WASPADA, 2 = BAHAYA.
"""
from dataclasses import dataclass
from typing import Callable, List, Optional

from search_algorithm import BuildingGraph, SearchResult

STATUS = {0: "AMAN", 1: "WASPADA", 2: "BAHAYA"}
JARAK_JAUH = 50.0  # meter


@dataclass
class Facts:
    graph: BuildingGraph
    start: str
    blocked: frozenset
    result: SearchResult
    baseline: SearchResult          # hasil pencarian jika tidak ada bahaya
    reachable_exits: int

    @property
    def start_name(self) -> str:
        return self.graph.nodes[self.start].name

    @property
    def start_blocked(self) -> bool:
        return self.start in self.blocked

    @property
    def already_at_exit(self) -> bool:
        return self.graph.nodes[self.start].is_exit and not self.start_blocked

    @property
    def uses_stairs(self) -> bool:
        p = self.result.path or []
        return any(self.graph.nodes[a].floor != self.graph.nodes[b].floor for a, b in zip(p, p[1:]))

    @property
    def detour(self) -> float:
        if not (self.result.found and self.baseline.found):
            return 0.0
        return round(self.result.distance - self.baseline.distance, 1)


@dataclass
class Rule:
    id: str
    level: int
    condition: Callable[[Facts], bool]
    message: Callable[[Facts], str]


RULES: List[Rule] = [
    Rule("R1", 2, lambda f: f.start_blocked,
         lambda f: f"Lokasi '{f.start_name}' terdampak bahaya. Segera menjauh dari area tersebut."),
    Rule("R2", 2, lambda f: not f.result.found and not f.already_at_exit,
         lambda f: "Tidak ada jalur menuju pintu keluar. Tetap di area aman, "
                   "beri tanda ke petugas, dan hubungi petugas keamanan atau 112."),
    Rule("R3", 1, lambda f: f.result.found and f.reachable_exits == 1 and not f.already_at_exit,
         lambda f: "Hanya 1 pintu keluar yang masih dapat dicapai. Ikuti rute dan jangan berbalik arah."),
    Rule("R4", 1, lambda f: f.result.found and (f.result.distance or 0) > JARAK_JAUH,
         lambda f: f"Jarak ke pintu keluar jauh ({f.result.distance} m). Berjalan cepat, jangan berlari."),
    Rule("R5", 1, lambda f: f.result.found and f.detour > 0 and bool(f.blocked),
         lambda f: f"Rute normal terhalang bahaya. Anda harus memutar (+{f.detour} m)."),
    Rule("R6", 0, lambda f: f.result.found and f.uses_stairs,
         lambda f: "Rute melewati tangga. Gunakan tangga, jangan gunakan lift."),
    Rule("R7", 0, lambda f: f.already_at_exit,
         lambda f: "Anda sudah berada di pintu keluar. Segera menjauh dari gedung."),
    Rule("R8", 0, lambda f: f.result.found and not f.blocked and not f.already_at_exit,
         lambda f: "Tidak ada area terdampak. Rute berikut adalah rute evakuasi normal."),
    Rule("R9", 1, lambda f: f.start == "kantin" and not f.already_at_exit,
         lambda f: "Anda berada di Kantin. Jika masih aman, matikan kompor/gas sebelum keluar."),
]
