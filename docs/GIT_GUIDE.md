# Panduan Git Kelompok AI-TE-103

| Peran | Nama | Branch |
|-------|------|--------|
| Manager / Ketua | Aditya Rizqi Mevian | `main` |
| Dev 1 | Matthew Fajar Sitorus | `dev-fajar` |
| Dev 2 | Matthew Asher Augusta | `dev-asher` |

## 1. Ketua (Aditya), sekali di awal

```bash
cd AI-TE-103
git init -b main
git add .
git commit -m "Initial commit: EvacRoute AI"
```

Buat repository kosong `AI-TE-103` di GitHub (tanpa README bawaan), lalu:

```bash
git remote add origin https://github.com/<username-aditya>/AI-TE-103.git
git push -u origin main
```

Di GitHub: **Settings > Collaborators > Add people**, tambahkan Fajar dan Asher.

## 2. Dev 1 (Fajar) dan Dev 2 (Asher)

```bash
git clone https://github.com/<username-aditya>/AI-TE-103.git
cd AI-TE-103
git checkout -b dev-fajar        # Asher: git checkout -b dev-asher
```

Kerjakan bagianmu, lalu:

```bash
python -m pytest
git add .
git commit -m "Tambah <apa yang dikerjakan>"
git push -u origin dev-fajar     # Asher: dev-asher
```

Buka GitHub, klik **Compare & pull request**, minta Aditya me-review.

## 3. Ketua me-review dan merge

Tab **Pull requests**, baca perubahan, klik **Merge pull request**. Lalu semua
anggota menjalankan:

```bash
git checkout main && git pull
git checkout dev-fajar && git merge main     # Asher: dev-asher
```

## Pembagian kerja

- **Fajar (Dev 1), bagian search:** pelajari `search_algorithm/`, tambah 1-2
  skenario tes baru di `tests/test_search.py`, dan buat `docs/ANALISIS.md`
  yang membandingkan BFS, UCS, A* (jarak, langkah, node diekspansi) pada
  beberapa lokasi awal dan skenario bahaya.
- **Asher (Dev 2), bagian expert system dan GUI:** pelajari `expert_system/`
  dan `app/gui.py`, tambah satu aturan baru di `rules.py` (misalnya peringatan
  jika rute melewati dapur/kantin) lengkap dengan tesnya, lalu coba GUI.
- **Aditya (Ketua):** review dan merge PR, memperbarui README akhir, dan
  menyiapkan presentasi/demo.

## Sebelum dikumpulkan

- README ada di `main` dan nama anggota benar.
- `python -m pytest` lolos di `main`.
- Setiap anggota punya commit atas namanya sendiri.
- Semua anggota bisa menjelaskan seluruh kode dan alur sistem.
