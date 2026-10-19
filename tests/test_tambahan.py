import os

import pytest

from expert_system import diagnose
from search_algorithm import ALGORITHMS, BuildingGraph

DATA = os.path.join(os.path.dirname(__file__), "..", "data", "gedung.json")


@pytest.fixture(scope="module")
def graph():
    return BuildingGraph.from_json(DATA)


# --- tes bagian search ---
@pytest.mark.parametrize("start", ["lab_komputer", "aula", "perpustakaan"])
def test_astar_expands_less_than_or_equal_ucs(graph, start):
    assert ALGORITHMS["A*"](graph, start).expanded <= ALGORITHMS["UCS"](graph, start).expanded


def test_all_algorithms_agree_goal_unreachable(graph):
    blocked = {"l2_tangga_a", "l2_tangga_b"}
    assert all(not f(graph, "aula", blocked).found for f in ALGORITHMS.values())


# --- tes bagian expert system (aturan R9) ---
def test_rule_kantin_warns(graph):
    d = diagnose(graph, "kantin")
    assert "R9" in d.fired_rules and d.status == "WASPADA"


def test_rule_kantin_not_fired_elsewhere(graph):
    assert "R9" not in diagnose(graph, "lobby").fired_rules
