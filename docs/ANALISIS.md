# Analisis Perbandingan Algoritma Search

Data dihasilkan dengan menjalankan BFS, UCS, dan A* pada denah di
`data/gedung.json`. **Diekspansi** = jumlah titik yang dicek algoritma
sebelum menemukan pintu keluar (makin kecil, makin hemat usaha).

## Hasil

| Skenario | Algoritma | Ketemu | Jarak (m) | Langkah | Diekspansi |
|----------|-----------|--------|-----------|---------|------------|
| Lab Komputer, normal | BFS | ya | 32.0 | 4 | 11 |
| | UCS | ya | 32.0 | 4 | 11 |
| | A* | ya | 32.0 | 4 | **5** |
| Aula, normal | BFS | ya | 52.0 | 6 | 13 |
| | UCS | ya | 52.0 | 6 | 13 |
| | A* | ya | 52.0 | 6 | **12** |
| Perpustakaan, normal | BFS | ya | 32.0 | 4 | 11 |
| | UCS | ya | 32.0 | 4 | 11 |
| | A* | ya | 32.0 | 4 | **5** |
| Lab Komputer, Tangga Barat L2 terblokir | BFS | ya | 52.0 | 6 | 10 |
| | UCS | ya | 52.0 | 6 | 10 |
| | A* | ya | 52.0 | 6 | **9** |
| Lobby, Pintu Keluar Utama terblokir | BFS | ya | 20.0 | 2 | 4 |
| | UCS | ya | 20.0 | 2 | 6 |
| | A* | ya | 20.0 | 2 | 4 |
| Aula, kedua tangga L2 terblokir | BFS/UCS/A* | tidak | - | - | 5 |

## Kesimpulan

1. **Jarak sama di gedung ini.** BFS, UCS, dan A* menghasilkan jarak yang sama
   di semua skenario. Penyebabnya, rute dengan langkah paling sedikit di gedung
   ini kebetulan juga rute terpendek. Pada gedung lain dengan jarak antar ruangan
   yang sangat bervariasi, BFS bisa menghasilkan rute yang lebih panjang daripada UCS.
2. **A\* paling hemat usaha.** A* mengekspansi lebih sedikit titik, paling terlihat
   di Lab Komputer (5 berbanding 11), karena heuristik jarak garis lurus
   mengarahkannya ke pintu keluar. Pada Aula selisihnya kecil (12 berbanding 13)
   karena posisi Aula jauh dan harus berbelok lewat tangga.
3. **UCS tidak selalu lebih hemat dari BFS.** Pada skenario Lobby dengan Pintu Keluar
   Utama terblokir, UCS mengekspansi 6 titik, sedangkan BFS hanya 4. UCS
   menjamin jarak terpendek, tetapi tidak menjamin pengecekan paling sedikit.
4. **Rute berubah saat ada bahaya.** Saat Tangga Barat L2 terblokir, Lab Komputer
   harus memutar lewat tangga timur: jarak naik dari 32.0 m menjadi 52.0 m.
5. **Kasus tanpa jalan keluar.** Jika kedua tangga lantai 2 terblokir, semua
   algoritma sama-sama menyimpulkan tidak ada rute. Sistem pakar lalu
   memberi status BAHAYA.

## Catatan

Angka di atas adalah hasil pada denah contoh. Kesimpulannya berlaku untuk denah
ini, belum tentu untuk gedung lain.
