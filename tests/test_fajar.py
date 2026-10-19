import os
import pytest
from search_algorithm import ALGORITHMS, BuildingGraph
DATA = os.path.join(os.path.dirname(__file__), "..", "data", "gedung.json")

@pytest.fixture(scope="module")
def graph():
 return BuildingGraph.from_json(DATA)

@pytest.mark.parametrize("name", list(ALGORITHMS))
def test_perpustakaan_tangga_timur_terblokir(graph, name):
  r = ALGORITHMS[name](graph, "perpustakaan", {"l2_tangga_b"})
  assert r.found
  assert "l2_tangga_b" not in r.path

def test_ucs_dan_astar_jarak_sama(graph):
 blocked = {"l2_tangga_b"}
 ucs = ALGORITHMS["UCS"](graph, "perpustakaan", blocked)
 astar = ALGORITHMS["A*"](graph, "perpustakaan", blocked)
 assert ucs.distance == astar.distance