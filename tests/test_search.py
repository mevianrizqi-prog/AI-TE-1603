import os

import pytest

from search_algorithm import ALGORITHMS, BuildingGraph

DATA = os.path.join(os.path.dirname(__file__), "..", "data", "gedung.json")


@pytest.fixture(scope="module")
def graph():
    return BuildingGraph.from_json(DATA)


@pytest.mark.parametrize("name", list(ALGORITHMS))
def test_path_is_valid(name, graph):
    r = ALGORITHMS[name](graph, "lab_komputer")
    assert r.found
    assert r.path[0] == "lab_komputer"
    assert graph.nodes[r.path[-1]].is_exit
    for a, b in zip(r.path, r.path[1:]):
        assert b in graph.adj[a]


def test_ucs_and_astar_same_distance(graph):
    for start in graph.nodes:
        assert ALGORITHMS["UCS"](graph, start).distance == ALGORITHMS["A*"](graph, start).distance


def test_bfs_has_fewest_hops(graph):
    for start in graph.nodes:
        b = ALGORITHMS["BFS"](graph, start)
        assert b.hops <= ALGORITHMS["UCS"](graph, start).hops


def test_astar_expands_not_more_than_ucs(graph):
    assert ALGORITHMS["A*"](graph, "aula").expanded <= ALGORITHMS["UCS"](graph, "aula").expanded


@pytest.mark.parametrize("name", list(ALGORITHMS))
def test_hazard_changes_route(name, graph):
    normal = ALGORITHMS[name](graph, "lab_komputer")
    hazard = ALGORITHMS[name](graph, "lab_komputer", {"l2_tangga_a"})
    assert hazard.found and "l2_tangga_a" not in hazard.path
    assert hazard.distance >= normal.distance


@pytest.mark.parametrize("name", list(ALGORITHMS))
def test_no_path_when_both_stairs_blocked(name, graph):
    assert not ALGORITHMS[name](graph, "aula", {"l2_tangga_a", "l2_tangga_b"}).found


@pytest.mark.parametrize("name", list(ALGORITHMS))
def test_blocked_exit_not_used(name, graph):
    r = ALGORITHMS[name](graph, "lobby", {"exit_utama"})
    assert r.found and r.path[-1] != "exit_utama"


@pytest.mark.parametrize("name", list(ALGORITHMS))
def test_start_at_exit(name, graph):
    r = ALGORITHMS[name](graph, "exit_utama")
    assert r.path == ["exit_utama"] and r.distance == 0
