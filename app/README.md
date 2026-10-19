# app

Bagian **tampilan (GUI)** EvacRoute AI, dibuat dengan **Tkinter** (library bawaan Python). GUI hanya menampilkan dan menerima masukan. Logika pencarian dan aturan ada di folder lain.

## Isi folder

| File | Fungsi |
|------|--------|
| `gui.py` | Jendela aplikasi: pilihan, denah, dan kotak hasil |

## Cara menjalankan

Dari folder utama proyek:

```bash
python main.py
```

Kebutuhan: Python 3.9+ dengan Tkinter. Windows dan macOS sudah menyertakannya. Di Linux: `sudo apt install python3-tk`.

## Isi tampilan

- **Lokasi Anda** dan **Algoritma** (BFS, UCS, A*).
- **Area terdampak bahaya**: daftar yang bisa dipilih lebih dari satu (tahan Ctrl).
- Tombol **Diagnosa** dan **Reset**.
- Dua denah, **Lantai 1** dan **Lantai 2**.
- Kotak hasil: status, rute, jarak, jumlah titik yang dicek, dan saran.

## Arti warna di denah

| Warna | Arti |
|-------|------|
| Hijau | Pintu keluar |
| Merah (lingkaran) | Area bahaya |
| Lingkaran bertepi biru | Lokasi pengguna |
| Kuning dan garis merah | Rute yang ditemukan |

Status ditampilkan berwarna: hijau (AMAN), oranye (WASPADA), merah (BAHAYA).

## Cara pakai

1. Pilih lokasi dan algoritma.
2. (Opsional) Pilih satu atau lebih area bahaya.
3. Klik **Diagnosa**.
4. Klik **Reset** untuk mengosongkan area bahaya.

## Cadangan tanpa GUI

```bash
python main.py --cli --start lab_komputer --block l2_tangga_a --algo "A*"
```

## Catatan rancangan

Tampilan sengaja dipisah dari logika. Fungsi yang dipanggil GUI adalah `diagnose` dari `expert_system`, sehingga logika yang sama bisa dites otomatis dan dijalankan lewat CLI tanpa membuka jendela.
