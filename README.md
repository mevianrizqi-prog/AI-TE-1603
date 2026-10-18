# AI-TE-103

**EvacRoute AI: Diagnosis Rute Evakuasi Gedung**
Tugas 1, Kecerdasan Buatan: Search Algorithm dan Expert System (rule-based)

| Peran | Nama | Branch |
|-------|------|--------|
| Manager / Ketua | Aditya Rizqi Mevian | `main` |
| Dev 1 | Matthew Fajar Sitorus | `dev-fajar` |
| Dev 2 | Matthew Asher Augusta | `dev-asher` |

## 1. Deskripsi

EvacRoute AI adalah aplikasi sederhana yang membantu menentukan rute evakuasi
tercepat dari suatu ruangan menuju pintu keluar terdekat pada model gedung dua
lantai. Pengguna dapat menandai area yang terdampak bahaya (misalnya kebakaran
atau lantai terblokir), lalu sistem mencari rute alternatif dan memberi status
serta saran keselamatan.

## 2. Tujuan

- Menerapkan algoritma pencarian (search) pada masalah nyata.
- Membandingkan algoritma uninformed (BFS, UCS) dan informed (A*).
- Menerapkan sistem pakar sederhana berbasis aturan untuk menafsirkan hasil pencarian.

## 3. Teknologi

- **Python 3.9+**: bahasa pemrograman utama.
- **Tkinter**: antarmuka grafis (GUI) yang menampilkan denah dan rute.
- **BFS, UCS, A\***: algoritma pencarian rute.
- **Rule-based expert system**: 8 aturan JIKA-MAKA untuk menentukan status dan saran.

## 4. Cara Kerja Sistem

1. Pengguna memilih lokasi awal, algoritma, dan area terdampak bahaya.
2. Gedung dibaca dari `data/gedung.json` sebagai **graf**: ruangan = node, jalur = edge berbobot (jarak meter; pindah lantai ditambah penalti tangga).
3. Algoritma mencari rute ke pintu keluar terdekat yang **tidak terblokir**, tanpa melewati area bahaya.
4. Hasil pencarian menjadi **fakta** untuk sistem pakar (apakah ada rute, berapa pintu keluar yang tersisa, seberapa jauh, apakah melewati tangga, apakah harus memutar).
5. Aturan yang cocok menghasilkan status **AMAN / WASPADA / BAHAYA** dan saran.
6. Rute digambar di denah.

| Algoritma | Jenis | Menghasilkan | Optimal? |
|-----------|-------|--------------|----------|
| BFS | Uninformed | Rute dengan jumlah langkah paling sedikit | Hanya untuk jumlah langkah |
| UCS | Uninformed | Rute dengan jarak (meter) terpendek | Ya |
| A* | Informed | Sama seperti UCS, dipandu heuristik jarak garis lurus | Ya |

**Informed vs uninformed:** BFS dan UCS tidak tahu arah pintu keluar. A* memakai
heuristik (jarak garis lurus pada denah ke pintu keluar terdekat), sehingga
biasanya mengekspansi lebih sedikit node.

## 5. Peran Kecerdasan Buatan

- **Search:** BFS, UCS, dan A* menjadi inti pencarian rute.
- **Expert system:** aturan di `expert_system/rules.py` menafsirkan hasil pencarian menjadi status dan saran.

Sistem ini berbasis algoritma dan aturan, **bukan** machine learning.

## 6. Batasan Sistem

- Denah gedung adalah model contoh di `data/gedung.json`, bukan gedung sebenarnya.
- Area bahaya dimasukkan manual oleh pengguna; sistem tidak mendeteksi api atau asap.
- Kepadatan orang, lebar jalur, dan kondisi lift tidak dimodelkan.
- Hasil hanya alat bantu belajar. Dalam keadaan darurat nyata, ikuti petunjuk petugas dan rambu evakuasi resmi.

## 7. Library / Kebutuhan

- Python 3.9 atau lebih baru.
- Tkinter (bawaan Python di Windows/macOS; Linux: `sudo apt install python3-tk`).
- `pytest` hanya untuk tes (`pip install -r requirements.txt`).

## 8. Cara Pakai

1. Jalankan aplikasi (lihat bagian 9).
2. Pilih **Lokasi Anda** dan **Algoritma**.
3. (Opsional) Pilih satu atau lebih **Area terdampak bahaya** di daftar.
4. Klik **Diagnosa**: status, rute, jarak, dan saran muncul, dan rute digambar di denah.
5. Klik **Reset** untuk mengosongkan area bahaya.

Skenario yang menarik untuk dicoba:
- Lokasi `Lab Komputer`, bahaya `Tangga Barat L2`: rute memutar lewat tangga timur (WASPADA).
- Lokasi `Aula`, bahaya `Tangga Barat L2` dan `Tangga Timur L2`: tidak ada rute (BAHAYA).
- Lokasi `Lobby`, bahaya `Pintu Keluar Barat` dan `Pintu Keluar Timur`: hanya 1 pintu keluar tersisa (WASPADA).

## 9. Cara Menjalankan

```bash
git clone https://github.com/<username>/AI-TE-103.git
cd AI-TE-103
pip install -r requirements.txt

python main.py                                   # GUI
python main.py --list                            # daftar id lokasi
python main.py --cli --start lab_komputer --block l2_tangga_a --algo A*   # tanpa GUI
python -m pytest                                 # jalankan tes
```

## 10. Struktur Folder

```
AI-TE-103/
├── search_algorithm/     # algoritma pencarian
│   ├── graph.py          # model gedung sebagai graf
│   └── algorithms.py     # BFS, UCS, A*
├── expert_system/        # sistem pakar berbasis aturan
│   ├── rules.py          # basis aturan (R1-R8)
│   └── engine.py         # mesin diagnosis
├── app/gui.py            # antarmuka Tkinter
├── data/gedung.json      # denah gedung
├── tests/                # tes otomatis
├── docs/GIT_GUIDE.md     # alur kerja Git kelompok
├── main.py               # titik masuk program
├── README.md
└── requirements.txt
```

## 11. Kontribusi

Lihat [docs/GIT_GUIDE.md](docs/GIT_GUIDE.md). Tiap anggota bekerja di branch
sendiri dan menggabungkannya ke `main` lewat pull request.

_AI Course Project: Search Algorithm and Expert System._
