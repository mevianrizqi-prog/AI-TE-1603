import os

import pytest

from expert_system import diagnose
from search_algorithm import BuildingGraph

DATA = os.path.join(os.path.dirname(__file__), "..", "data", "gedung.json")


@pytest.fixture(scope="module")
def graph():
    return BuildingGraph.from_json(DATA)


def test_normal_is_aman(graph):
    d = diagnose(graph, "lobby")
    assert d.status == "AMAN" and "R8" in d.fired_rules


def test_stairs_advice(graph):
    d = diagnose(graph, "lab_komputer")
    assert "R6" in d.fired_rules


def test_detour_is_waspada(graph):
    d = diagnose(graph, "lab_komputer", {"l2_tangga_a"}, "UCS")
    assert d.status == "WASPADA" and "R5" in d.fired_rules


def test_trapped_is_bahaya(graph):
    d = diagnose(graph, "aula", {"l2_tangga_a", "l2_tangga_b"})
    assert d.status == "BAHAYA" and "R2" in d.fired_rules and not d.result.found


def test_start_in_hazard_is_bahaya(graph):
    d = diagnose(graph, "kantin", {"kantin"})
    assert d.status == "BAHAYA" and "R1" in d.fired_rules


def test_single_exit_is_waspada(graph):
    d = diagnose(graph, "lobby", {"exit_barat", "exit_timur"})
    assert d.status == "WASPADA" and "R3" in d.fired_rules


def test_already_at_exit(graph):
    d = diagnose(graph, "exit_barat")
    assert "R7" in d.fired_rules and d.status == "AMAN"


def test_unknown_inputs(graph):
    with pytest.raises(KeyError):
        diagnose(graph, "tidak_ada")
    with pytest.raises(KeyError):
        diagnose(graph, "lobby", algorithm="XYZ")
