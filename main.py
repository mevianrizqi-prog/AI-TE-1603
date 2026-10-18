"""EvacRoute AI - titik masuk program.

    python main.py                      -> buka GUI (Tkinter)
    python main.py --cli --start lab_komputer --block l2_tangga_a --algo A*
    python main.py --list               -> daftar id lokasi
"""
import argparse
import os

from expert_system import diagnose
from search_algorithm import ALGORITHMS, BuildingGraph

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "gedung.json")


def main():
    p = argparse.ArgumentParser(description="EvacRoute AI: diagnosis rute evakuasi gedung.")
    p.add_argument("--cli", action="store_true", help="jalankan tanpa GUI")
    p.add_argument("--list", action="store_true", help="tampilkan id semua lokasi")
    p.add_argument("--start", default="lab_komputer", help="id lokasi awal")
    p.add_argument("--block", default="", help="id area bahaya, pisahkan dengan koma")
    p.add_argument("--algo", default="BFS", choices=list(ALGORITHMS))
    a = p.parse_args()

    graph = BuildingGraph.from_json(DATA)
    if a.list:
        for i, n in graph.nodes.items():
            print(f"{i:<14} {n.name} (lantai {n.floor})")
        return
    if a.cli:
        blocked = [b for b in a.block.split(",") if b]
        d = diagnose(graph, a.start, blocked, a.algo)
        print(f"Status : {d.status}")
        print("Rute   : " + (" -> ".join(d.path_names) if d.result.found else "tidak ditemukan"))
        if d.result.found:
            print(f"Jarak  : {d.result.distance} m, langkah {d.result.hops}, diekspansi {d.result.expanded}")
        print("Saran  :")
        for m in d.messages:
            print(f"  - {m}")
        return
    from app.gui import launch
    launch(graph)


if __name__ == "__main__":
    main()
