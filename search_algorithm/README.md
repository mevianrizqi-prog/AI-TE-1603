# search_algorithm

Bagian **pencarian rute** EvacRoute AI. Folder ini mengubah gedung menjadi peta titik dan garis, lalu mencari rute ke pintu keluar terdekat.

## Isi folder

| File | Fungsi |
|------|--------|
| `graph.py` | Mengubah gedung (`data/gedung.json`) menjadi graf |
| `algorithms.py` | Tiga algoritma pencarian: BFS, UCS, A* |
| `__init__.py` | Mengumpulkan semuanya, termasuk daftar `ALGORITHMS` |

## Konsep dasar

- **Titik (node)** = tempat, misalnya Lobby, Lab Komputer, Tangga, Pintu Keluar.
- **Garis (edge)** = jalan antar tempat, dengan jarak dalam meter.
- Jarak dihitung otomatis dari posisi dua titik. Pindah lantai lewat tangga ditambah **8 meter**.
- **Area bahaya** adalah titik yang tidak boleh dilewati. Fungsi `neighbors` hanya memberi tetangga yang tidak terblokir.
- **Tujuan** adalah pintu keluar mana pun yang tidak terblokir.

## Tiga algoritma

| Algoritma | Cara memilih tempat yang dicek | Hasil |
|-----------|--------------------------------|-------|
| **BFS** | Yang terdekat dulu, selapis demi selapis (antrean) | Langkah paling sedikit |
| **UCS** | Yang jaraknya paling kecil dulu | Jarak (meter) terpendek |
| **A\*** | Jarak tempuh + perkiraan sisa jarak (heuristik) | Jarak terpendek, pengecekan lebih sedikit |

- BFS dan UCS termasuk **uninformed search** (tidak tahu arah tujuan).
- A* termasuk **informed search**. Heuristiknya adalah jarak garis lurus di denah ke pintu keluar terdekat, yang tidak pernah melebihi jarak sebenarnya, sehingga hasil A* tetap yang terpendek.

## Hasil pencarian

Setiap algoritma mengembalikan `SearchResult` dengan isi:

- `path`: daftar titik dari awal ke pintu keluar (`None` jika tidak ada rute)
- `distance`: jarak total (meter)
- `hops`: jumlah langkah
- `expanded`: jumlah titik yang dicek (makin kecil makin hemat usaha)
- `found`: `True` jika rute ditemukan

## Contoh pemakaian

```python
from search_algorithm import BuildingGraph, ALGORITHMS

graph = BuildingGraph.from_json("data/gedung.json")
hasil = ALGORITHMS["A*"](graph, "lab_komputer", {"l2_tangga_a"})

print(hasil.path)
print(hasil.distance, hasil.expanded)
```

## Tes

Tes folder ini ada di `tests/test_search.py`, `tests/test_tambahan.py`, dan `tests/test_fajar.py`.

```bash
python -m pytest
```
