import os

import pytest

from expert_system import diagnose 
from search_algorithm import BuildingGraph

DATA = os.path.join(os.path.dirname(__file__), "..", "data", "gedung.json")


@pytest.fixture(scope="module") 
def graph():
    return BuildingGraph.from_json(DATA) 


def test_dua_area_bahaya_memicu_r10(graph):
    d = diagnose(graph, "lobby", {"kelas_101", "kelas_102"})
    assert "R10" in d.fired_rules
    assert d.status == "WASPADA"


def test_satu_area_bahaya_tidak_memicu_r10(graph):
    d = diagnose(graph, "lobby", {"kelas_101"})
    assert "R10" not in d.fired_rules