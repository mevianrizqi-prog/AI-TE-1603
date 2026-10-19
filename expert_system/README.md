# expert_system

Bagian **sistem pakar** EvacRoute AI. Folder ini menafsirkan hasil pencarian rute menjadi status **AMAN / WASPADA / BAHAYA** dan saran keselamatan, memakai aturan JIKA-MAKA.

## Isi folder

| File | Fungsi |
|------|--------|
| `rules.py` | Basis aturan (R1 sampai R10) dan fakta yang dipakai aturan |
| `engine.py` | Mesin diagnosis: menjalankan search, mengumpulkan fakta, menerapkan aturan |
| `__init__.py` | Mengekspor `diagnose` dan `RULES` |

## Cara kerja

1. `diagnose` menjalankan search dengan area bahaya, dan sekali lagi tanpa bahaya sebagai pembanding.
2. Hasilnya dikumpulkan menjadi **fakta**: ada rute atau tidak, berapa pintu keluar tersisa, jarak, apakah lewat tangga, dan berapa meter harus memutar.
3. Semua aturan dicek terhadap fakta.
4. Status akhir adalah **tingkat paling parah** dari aturan yang cocok (0 = AMAN, 1 = WASPADA, 2 = BAHAYA).
5. Pesan dari semua aturan yang cocok dikumpulkan sebagai saran.

## Daftar aturan

| Aturan | Kondisi | Tingkat |
|--------|---------|---------|
| R1 | Lokasi pengguna terkena bahaya | BAHAYA |
| R2 | Tidak ada jalur ke pintu keluar | BAHAYA |
| R3 | Hanya 1 pintu keluar yang masih bisa dicapai | WASPADA |
| R4 | Jarak ke pintu keluar lebih dari 50 m | WASPADA |
| R5 | Rute normal terhalang, harus memutar | WASPADA |
| R6 | Rute melewati tangga (jangan pakai lift) | info |
| R7 | Pengguna sudah di pintu keluar | AMAN |
| R8 | Tidak ada area terdampak | AMAN |
| R9 | Pengguna berada di Kantin (matikan kompor/gas) | WASPADA |
| R10 | Dua area bahaya atau lebih sekaligus | WASPADA |

## Bentuk sebuah aturan

```python
Rule("R10", 1, lambda f: len(f.blocked) >= 2,
     lambda f: "pesan saran ...")
```

Artinya: aturan bernama R10, tingkat 1 (WASPADA). JIKA kondisi (`lambda` pertama) benar, MAKA tampilkan pesan (`lambda` kedua). Fakta `f` berisi hal seperti `f.blocked` (area bahaya) dan `f.result` (hasil search).

## Contoh pemakaian

```python
from search_algorithm import BuildingGraph
from expert_system import diagnose

graph = BuildingGraph.from_json("data/gedung.json")
d = diagnose(graph, "lab_komputer", {"l2_tangga_a"}, "A*")

print(d.status)
print(d.path_names)
for pesan in d.messages:
    print("-", pesan)
```

## Menambah aturan baru

1. Buka `rules.py`.
2. Tambahkan `Rule(...)` baru di dalam daftar `RULES`, **sebelum** tanda `]` terakhir. Gunakan 4 spasi di awal baris dan beri koma di ujungnya.
3. Tambahkan tes di folder `tests/`.

## Tes

`tests/test_expert.py`, `tests/test_tambahan.py`, dan `tests/test_asher.py`.
