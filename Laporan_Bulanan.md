# LAPORAN ANALISIS PENJUALAN BULANAN
## PT Mensana Aneka Satwa
### Periode: Januari - Maret 2026

---

**Disusun oleh:** Tim Data Analyst
**Tanggal:** 8 Juli 2026
**Data:** 10 Cabang Distributor | 15 Produk Unggulan | 3 Bulan

---

## DAFTAR ISI

1. [Executive Summary](#1-executive-summary)
2. [Input - Data Mentah](#2-input---data-mentah)
3. [Proses - Transformasi & Agregasi](#3-proses---transformasi--agregasi)
4. [Total Omset 3 Bulan](#4-total-omset-3-bulan)
5. [Analisis per Bulan](#5-analisis-per-bulan)
6. [Progress Omset Tiap Cabang](#6-progress-omset-tiap-cabang)
7. [Ranking Cabang](#7-ranking-cabang)
8. [Produk Terlaris](#8-produk-terlaris)
9. [Analisis Kategori Produk](#9-analisis-kategori-produk)
10. [Pola Hari Kerja vs Akhir Pekan](#10-pola-hari-kerja-vs-akhir-pekans)
11. [Dampak Hari Libur Nasional](#11-dampak-hari-libur-nasional)
12. [Mix Produk per Cabang](#12-mix-produk-per-cabang)
13. [Efisiensi Harga](#13-efisiensi-harga)
14. [Proyeksi Penjualan Q2](#14-proyeksi-penjualan-q2)
15. [Kesimpulan & Rekomendasi](#15-kesimpulan--rekomendasi)

---

## 1. EXECUTIVE SUMMARY

> **Total Omset Januari - Maret 2026: Rp 2,32 Miliar** dari 10 cabang distributor di seluruh Indonesia.

| Metrik | Q1 2026 |
|--------|---------|
| Total Omset | Rp 2.320.386.997 |
| Total Kuantiti | 20.892 unit |
| Rata-rata Omset/Bulan | Rp 773.462.332 |
| Rata-rata Omset/Cabang/Bulan | Rp 77.346.233 |
| Cabang Tertinggi | Jakarta (Rp 369,98 juta) |
| Cabang Terendah | Pontianak (Rp 136,13 juta) |
| Produk Terlaris | Masamix (Rp 228,85 juta) |
| Kategori Terlaris | Vitamin (39,4%) |

### Temuan Kunci:
1. **Februari mengalami penurunan** - turun 11,1% dari Januari karena jumlah hari lebih sedikit (28 hari)
2. **Maret recovery kuat** - naik 17,4% dari Februari, tertinggi dalam Q1
3. **Disparitas cabang signifikan** - Jakarta 2,72x lebih besar dari Pontianak
4. **Vitamin dominasi** - 39,4% total omset dari 6 produk
5. **Weekend turun drastis** - penjualan Sabtu-Minggu ~48% lebih rendah dari hari kerja
6. **Hari libur berdampak besar** - penurunan 45-49% saat libur nasional

---

## 2. INPUT - DATA MENTAH

### Sumber Data
Data penjualan harian 10 cabang distributor PT Mensana Aneka Satwa selama 3 bulan (Januari - Maret 2026), diagregasi menjadi data bulanan untuk analisis ini.

### Komponen Data

| Komponen | Jumlah |
|----------|--------|
| Cabang Distributor | 10 |
| Produk Unggulan | 15 (6 Vitamin, 4 Antibiotik, 1 Premix, 1 Herbal, 1 Antikoksidiosis, 2 Desinfektan) |
| Periode | 3 bulan (Januari - Maret 2026) |
| Total Records Harian | ~13.500 |

### Hari Libur Nasional (Q1 2026)

| Tanggal | Hari Libur | Bulan |
|---------|-----------|-------|
| 1 Januari 2026 | Tahun Baru | Januari |
| 29 Januari 2026 | Isra Mi'raj | Januari |
| 17 Februari 2026 | Tahun Baru Imlek | Februari |
| 19 Maret 2026 | Nyepi | Maret |

---

## 3. PROSES - TRANSFORMASI & AGREGASI

### Masalah Inti
> Setiap cabang menggunakan **kode dan nama produk yang berbeda-beda** untuk produk yang sama.

**Contoh Produk "Supralit":**
- Medan: `MED-V-001 / Supralit Anti Stress`
- Jakarta: `JKT-VA-001 / Supralit Powder`
- Bandung: `BDG/01/V / Anti-Stress Powder`

### Solusi: Mapping Table + Agregasi Bulanan

```
[DATA HARIAN]     [MAPPING & KONSOLIDASI]     [AGREGASI BULANAN]
13.500 record  --> Kode per cabang ke    -->  Total Omset per
(10 cabang x       kode standar               bulan, cabang,
 15 produk x       (MSV-001, dll)             produk, kategori
 90 hari)
```

---

## 4. TOTAL OMSET 3 BULAN

### Ringkasan Keseluruhan

| Metrik | Nilai |
|--------|-------|
| **Total Omset** | **Rp 2.320.386.997** |
| Total Kuantiti | 20.892 unit |
| Rata-rata Omset/Bulan | Rp 773.462.332 |
| Rata-rata Omset/Cabang/Bulan | Rp 77.346.233 |

---

## 5. ANALISIS PER BULAN

### Tren Omset Bulanan

| Bulan | Total Omset | Hari | vs Bulan Sebelumnya | Keterangan |
|-------|------------|------|---------------------|------------|
| Januari | Rp 791.154.480 | 31 | - | Libur: Tahun Baru (1 Jan), Isra Mi'raj (29 Jan) |
| Februari | Rp 703.493.151 | 28 | -11,1% | Libur: Imlek (17 Feb), hari lebih sedikit |
| Maret | Rp 825.739.366 | 31 | +17,4% | Libur: Nyepi (19 Mar), recovery kuat |

> **Insight:** Pola bulanan menunjukkan **seasonal dip di Februari** karena: (1) jumlah hari lebih sedikit (28 vs 31 hari), (2) adanya hari libur Imlek. **Maret recovery kuat** dengan peningkatan 17,4%, menunjukkan permintaan yang tertunda terpenuhi.

### Rata-rata Omset Harian per Bulan

| Bulan | Rata-rata/Hari | Keterangan |
|-------|----------------|------------|
| Januari | ~Rp 25,5 juta | Stabil, 2 hari libur |
| Februari | ~Rp 25,1 juta | Stabil, 1 hari libur |
| Maret | ~Rp 26,6 juta | Tertinggi, 1 hari libur |

> **Insight:** Rata-rata omset per hari **meningkat di Maret** (Rp 26,6 juta) dibanding Januari-Februari. Ini menunjukkan tren positif menjelang Q2.

---

## 6. PROGRESS OMSET TIAP CABANG

### Progress Bulanan per Cabang (Rp)

| Cabang | Januari | Februari | Maret | Total Q1 | Growth Jan-Feb | Growth Feb-Mar |
|--------|---------|----------|-------|----------|----------------|----------------|
| Jakarta | ~Rp 124 juta | ~Rp 110 juta | ~Rp 136 juta | Rp 369,98 juta | -11,3% | +23,6% |
| Surabaya | ~Rp 101 juta | ~Rp 90 juta | ~Rp 110 juta | Rp 300,75 juta | -10,9% | +22,2% |
| Bandung | ~Rp 87 juta | ~Rp 78 juta | ~Rp 96 juta | Rp 260,46 juta | -10,3% | +23,1% |
| Medan | ~Rp 84 juta | ~Rp 76 juta | ~Rp 92 juta | Rp 251,70 juta | -9,5% | +21,1% |
| Makassar | ~Rp 84 juta | ~Rp 76 juta | ~Rp 91 juta | Rp 250,79 juta | -9,5% | +20,0% |
| Semarang | ~Rp 83 juta | ~Rp 75 juta | ~Rp 90 juta | Rp 247,93 juta | -9,6% | +20,0% |
| Palembang | ~Rp 60 juta | ~Rp 54 juta | ~Rp 65 juta | Rp 178,44 juta | -10,0% | +20,4% |
| Padang | ~Rp 58 juta | ~Rp 52 juta | ~Rp 62 juta | Rp 172,00 juta | -10,3% | +19,2% |
| Denpasar | ~Rp 51 juta | ~Rp 46 juta | ~Rp 55 juta | Rp 152,22 juta | -9,8% | +19,6% |
| Pontianak | ~Rp 46 juta | ~Rp 42 juta | ~Rp 49 juta | Rp 136,13 juta | -8,7% | +16,7% |

> **Insight:** Semua cabang menunjukkan pola yang konsisten: **turun di Februari, naik di Maret**. Growth rate Februari-Maret cukup tinggi (+17-24%) menunjukkan adanya demand yang tertunda selama periode libur.

---

## 7. RANKING CABANG

### Ranking Q1 2026

| Rank | Cabang | Provinsi | Total Omset | % Total | Rata-rata/Bulan | Status |
|------|--------|----------|------------|---------|-----------------|--------|
| 1 | Jakarta | DKI Jakarta | Rp 369.977.238 | 15,9% | Rp 123,3 juta | Top Performer |
| 2 | Surabaya | Jawa Timur | Rp 300.746.237 | 13,0% | Rp 100,3 juta | Top Performer |
| 3 | Bandung | Jawa Barat | Rp 260.462.839 | 11,2% | Rp 86,8 juta | Good |
| 4 | Medan | Sumatera Utara | Rp 251.699.464 | 10,8% | Rp 83,9 juta | Good |
| 5 | Makassar | Sulawesi Selatan | Rp 250.787.565 | 10,8% | Rp 83,6 juta | Good |
| 6 | Semarang | Jawa Tengah | Rp 247.926.039 | 10,7% | Rp 82,6 juta | Good |
| 7 | Palembang | Sumatera Selatan | Rp 178.443.705 | 7,7% | Rp 59,5 juta | Needs Improvement |
| 8 | Padang | Sumatera Barat | Rp 172.000.578 | 7,4% | Rp 57,3 juta | Needs Improvement |
| 9 | Denpasar | Bali | Rp 152.216.908 | 6,6% | Rp 50,7 juta | Needs Improvement |
| 10 | Pontianak | Kalimantan Barat | Rp 136.126.424 | 5,9% | Rp 45,4 juta | Needs Improvement |

### Segmenasi Cabang

| Segmen | Cabang | Total Omset | % Total |
|--------|--------|------------|---------|
| **Top Performer** | Jakarta, Surabaya | Rp 670,7 juta | 28,9% |
| **Good** | Bandung, Medan, Makassar, Semarang | Rp 1.010,9 juta | 43,6% |
| **Needs Improvement** | Palembang, Padang, Denpasar, Pontianak | Rp 638,8 juta | 27,5% |

> **Insight:** Top 2 cabang (Jakarta + Surabaya) menyumbang hampir **29% total omset**. 4 cabang "Needs Improvement" menyumbang 27,5% - ada potensi peningkatan signifikan jika performa mereka bisa ditingkatkan ke level "Good".

---

## 8. PRODUK TERLARIS

### Ranking 15 Produk Q1 2026

| Rank | Produk | Kategori | Total Omset | % Total | Harga Standar |
|------|--------|----------|------------|---------|---------------|
| 1 | Masamix | Premix | Rp 228.846.650 | 9,9% | Rp 167.000 |
| 2 | Biomas Herbal | Herbal | Rp 212.445.693 | 9,2% | Rp 155.000 |
| 3 | Moxacol Forte | Antibiotik | Rp 203.357.129 | 8,8% | Rp 145.000 |
| 4 | Egg Promotor | Vitamin | Rp 189.553.310 | 8,2% | Rp 135.000 |
| 5 | Supralit Plus | Vitamin | Rp 174.637.321 | 7,5% | Rp 125.000 |
| 6 | Vitamas | Vitamin | Rp 162.549.260 | 7,0% | Rp 110.000 |
| 7 | Doxerin Plus | Antibiotik | Rp 158.946.250 | 6,8% | Rp 119.000 |
| 8 | GlutaMas | Desinfektan | Rp 155.118.460 | 6,7% | Rp 97.000 |
| 9 | Enromas | Antibiotik | Rp 131.583.152 | 5,7% | Rp 92.000 |
| 10 | Coxy-Mas | Antikoksidiosis | Rp 123.459.861 | 5,3% | Rp 88.000 |
| 11 | Colimas | Antibiotik | Rp 111.900.533 | 4,8% | Rp 78.000 |
| 12 | Masavit | Vitamin | Rp 108.142.310 | 4,7% | Rp 105.000 |
| 13 | Vitapoult | Vitamin | Rp 107.964.190 | 4,7% | Rp 95.000 |
| 14 | Supralit | Vitamin | Rp 87.390.210 | 3,8% | Rp 85.000 |
| 15 | Septocid | Desinfektan | Rp 81.438.141 | 3,5% | Rp 72.000 |

### Top 5 vs Bottom 5

| Kategori | Total Omset | % Total |
|----------|------------|---------|
| **Top 5 Produk** | Rp 1.008,8 juta | 43,5% |
| **Bottom 5 Produk** | Rp 510,3 juta | 22,0% |

> **Insight:** Top 5 produk menyumbang **43,5% total omset**. Masamix (Premix) menjadi produk terlaris meski hanya 1 produk di kategorinya - didukung harga satuan tertinggi (Rp 167.000).

---

## 9. ANALISIS KATEGORI PRODUK

### Distribusi Omset per Kategori

| Kategori | Total Omset | % Total | Jumlah Produk | Rata-rata/Produk |
|----------|------------|---------|---------------|-------------------|
| Vitamin | Rp 913.291.128 | 39,4% | 6 | Rp 152,2 juta |
| Antibiotik | Rp 605.787.064 | 26,1% | 4 | Rp 151,4 juta |
| Desinfektan | Rp 236.556.601 | 10,2% | 2 | Rp 118,3 juta |
| Premix | Rp 228.846.650 | 9,9% | 1 | Rp 228,8 juta |
| Herbal | Rp 212.445.693 | 9,2% | 1 | Rp 212,4 juta |
| Antikoksidiosis | Rp 123.459.861 | 5,3% | 1 | Rp 123,5 juta |

> **Insight:** **Vitamin mendominasi** dengan 39,4% dari 6 produk. **Premix** meski hanya 1 produk menyumbang 9,9% - menunjukkan harga satuan tinggi dan permintaan kuat. **Antibiotik** konsisten sebagai contributor kedua terbesar.

### Tren Kategori per Bulan

| Kategori | Januari | Februari | Maret | Trend |
|----------|---------|----------|-------|-------|
| Vitamin | ~Rp 304 juta | ~Rp 283 juta | ~Rp 326 juta | Naik |
| Antibiotik | ~Rp 202 juta | ~Rp 187 juta | ~Rp 217 juta | Naik |
| Desinfektan | ~Rp 79 juta | ~Rp 73 juta | ~Rp 85 juta | Naik |
| Premix | ~Rp 76 juta | ~Rp 71 juta | ~Rp 82 juta | Naik |
| Herbal | ~Rp 71 juta | ~Rp 66 juta | ~Rp 76 juta | Naik |
| Antikoksidiosis | ~Rp 41 juta | ~Rp 38 juta | ~Rp 44 juta | Naik |

> **Insight:** Semua kategori menunjukkan **recovery di Maret** setelah seasonal dip di Februari. Pola ini konsisten di semua kategori.

---

## 10. POLA HARI KERJA vs AKHIR PEKAN

### Perbandingan

| Tipe Hari | Rata-rata Omset | Index (Senin=100) | Persentase dari Total |
|-----------|-----------------|-------------------|----------------------|
| Hari Kerja (Sen-Jum) | ~Rp 28,5 juta/hari | 100 | ~73% |
| Akhir Pekan (Sab-Ming) | ~Rp 14,7 juta/hari | 52 | ~27% |

### Pola Harian

| Hari | Rata-rata Omset | Index | Keterangan |
|------|-----------------|-------|------------|
| Senin | ~Rp 30,1 juta | 100 | Tertinggi - restocking awal pekan |
| Selasa | ~Rp 29,5 juta | 98 | Stabil |
| Rabu | ~Rp 29,2 juta | 97 | Stabil |
| Kamis | ~Rp 28,8 juta | 96 | Stabil |
| Jumat | ~Rp 26,5 juta | 88 | Lebih rendah - pre-weekend |
| Sabtu | ~Rp 17,2 juta | 57 | Turun drastis |
| Minggu | ~Rp 12,1 juta | 40 | Terendah |

> **Insight:** **Senin memiliki omset tertinggi** karena efek restocking awal pekan. **Jumat sedikit lebih rendah** karena pelanggan menunda pembelian. **Sabtu-Minggu turun 43-60%** karena sebagian besar cabang beroperasi terbatas.

---

## 11. DAMPAK HARI LIBUR NASIONAL

### Analisis 4 Hari Libur Q1 2026

| Tanggal | Hari Libur | Omset Hari Libur | Omset Normal (rata-rata) | Penurunan |
|---------|-----------|-------------------|--------------------------|-----------|
| 1 Januari | Tahun Baru | Rp 14.045.816 | ~Rp 25,8 juta | -45,5% |
| 29 Januari | Isra Mi'raj | Rp 14.223.154 | ~Rp 25,8 juta | -44,9% |
| 17 Februari | Tahun Baru Imlek | Rp 13.081.700 | ~Rp 25,8 juta | -49,3% |
| 19 Maret | Nyepi | Rp 13.618.728 | ~Rp 25,8 juta | -47,2% |

> **Insight:** Hari libur nasional menyebabkan **penurunan omset 45-49%**. Efek ini terjadi karena: (1) Sebagian besar cabang tutup, (2) Distribusi terhenti, (3) Pelanggan tidak melakukan pembelian. **Recovery 1-2 hari setelah libur** menunjukkan adanya pembelian tertunda.

---

## 12. MIX PRODUK PER CABANG

### Proporsi Kategori per Cabang

| Cabang | Vitamin | Antibiotik | Premix | Herbal | Antikoksidiosis | Desinfektan |
|--------|---------|-----------|--------|--------|-----------------|-------------|
| Jakarta | ~39% | ~26% | ~10% | ~9% | ~5% | ~10% |
| Surabaya | ~39% | ~26% | ~10% | ~9% | ~5% | ~10% |
| Bandung | ~39% | ~26% | ~10% | ~9% | ~5% | ~10% |
| Medan | ~39% | ~26% | ~10% | ~9% | ~5% | ~10% |
| Semarang | ~39% | ~26% | ~10% | ~9% | ~5% | ~10% |
| Makassar | ~39% | ~26% | ~10% | ~9% | ~5% | ~10% |
| Palembang | ~39% | ~26% | ~10% | ~9% | ~5% | ~10% |
| Padang | ~39% | ~26% | ~10% | ~9% | ~5% | ~10% |
| Denpasar | ~39% | ~26% | ~10% | ~9% | ~5% | ~10% |
| Pontianak | ~39% | ~26% | ~10% | ~9% | ~5% | ~10% |

> **Insight:** Mix produk **relatif konsisten** antar cabang. Peluang untuk **menyesuaikan mix** berdasarkan karakteristik pasar lokal (misal: Denpasar lebih banyak herbal untuk pariwisata, Pontianak lebih banyak antibiotik untuk unggas).

---

## 13. EFISIENSI HARGA

### Variasi Harga Jual vs Harga Standar

| Produk | Harga Standar | Rata-rata Jual | Deviasi | Status |
|--------|--------------|----------------|---------|--------|
| Supralit | Rp 85.000 | ~Rp 85.000 | ~0% | Sesuai |
| Supralit Plus | Rp 125.000 | ~Rp 125.000 | ~0% | Sesuai |
| Vitapoult | Rp 95.000 | ~Rp 95.000 | ~0% | Sesuai |
| Vitamas | Rp 110.000 | ~Rp 110.000 | ~0% | Sesuai |
| Egg Promotor | Rp 135.000 | ~Rp 135.000 | ~0% | Sesuai |
| Colimas | Rp 78.000 | ~Rp 78.000 | ~0% | Sesuai |
| Doxerin Plus | Rp 119.000 | ~Rp 119.000 | ~0% | Sesuai |
| Enromas | Rp 92.000 | ~Rp 92.000 | ~0% | Sesuai |
| Moxacol Forte | Rp 145.000 | ~Rp 145.000 | ~0% | Sesuai |
| Masamix | Rp 167.000 | ~Rp 167.000 | ~0% | Sesuai |
| Biomas Herbal | Rp 155.000 | ~Rp 155.000 | ~0% | Sesuai |
| Coxy-Mas | Rp 88.000 | ~Rp 88.000 | ~0% | Sesuai |
| GlutaMas | Rp 97.000 | ~Rp 97.000 | ~0% | Sesuai |
| Septocid | Rp 72.000 | ~Rp 72.000 | ~0% | Sesuai |
| Masavit | Rp 105.000 | ~Rp 105.000 | ~0% | Sesuai |

> **Insight:** Variasi harga jual terhadap harga standar **sangat kecil (<0,1%)**. Harga jual sudah sangat konsisten dengan harga standar perusahaan. Strategi pricing sudah berjalan baik.

---

## 14. PROYEKSI PENJUALAN Q2

### Proyeksi April - Juni 2026

| Metrik | Q1 2026 (Aktual) | Q2 2026 (Proyeksi) | Pertumbuhan |
|--------|------------------|-------------------|-------------|
| Total Omset | Rp 2.320.386.997 | ~Rp 2.471.000.000 | +6,5% |
| Rata-rata/Bulan | Rp 773.462.332 | ~Rp 823.700.000 | +6,5% |
| Total Kuantiti | 20.892 unit | ~22.250 unit | +6,5% |

### Asumsi Proyeksi
- Q2 memiliki **92 hari** (vs 90 hari Q1)
- **Musim kemarau** meningkatkan penjualan vitamin
- **Libur nasional Q2:**
  - 1 April: Wafat Isa Almasih
  - 1 Mei: Hari Buruh
  - 26 Mei: Kenaikan Isa Almasih
  - 1 Juni: Hari Lahir Pancasila

### Proyeksi per Bulan Q2

| Bulan | Proyeksi Omset | Keterangan |
|-------|---------------|------------|
| April | ~Rp 800 juta | Recovery Q1, libur Wafat Isa Almasih |
| Mei | ~Rp 830 juta | Hari Buruh (1 Mei), Kenaikan Isa Almasih (26 Mei) |
| Juni | ~Rp 841 juta | Hari Pancasila (1 Juni), akhir kuartal |

---

## 15. KESIMPULAN & REKOMENDASI

### Kesimpulan Utama

1. **Total omset Q1 2026: Rp 2,32 miliar** - performa solid untuk 10 cabang
2. **Pola bulanan konsisten:** Februari turun (-11,1%), Maret recovery (+17,4%)
3. **Jakarta & Surabaya dominasi** - 28,9% total omset dari 2 cabang
4. **Vitamin produk utama** - 39,4% total omset dari 6 produk
5. **Weekend turun drastis** - ~48% lebih rendah dari hari kerja
6. **Hari libur berdampak besar** - penurunan 45-49%
7. **Harga konsisten** - deviasi <0,1% dari standar

### Rekomendasi Strategis

| No | Rekomendasi | Prioritas | Estimasi Dampak |
|----|------------|-----------|-----------------|
| 1 | **Optimasi 4 Cabang Bottom** - Fokus peningkatan Pontianak, Denpasar, Padang, Palembang | Tinggi | +10-15% omset cabang |
| 2 | **Promosi Weekend** - Program khusus Sabtu-Minggu | Sedang | +5-10% omset weekend |
| 3 | **Pre-Stocking Sebelum Libur** - Siapkan stok 2-3 hari sebelum libur nasional | Tinggi | Mengurangi stockout |
| 4 | **Diversifikasi Mix Produk** - Sesuaikan proporsi berdasarkan pasar lokal | Sedang | +5-8% omset |
| 5 | **Review Pricing** - Evaluasi margin produk premium | Rendah | +2-3% margin |
| 6 | **Forecasting System** - Implementasi prediksi penjualan | Sedang | Optimalisasi stok |
| 7 | **Dashboard Monitoring** - Real-time monitoring bulanan | Tinggi | Keputusan lebih cepat |

---

## LAMPIRAN

### A. Daftar 10 Cabang

| ID | Nama Cabang | Provinsi |
|----|------------|----------|
| CAB-01 | Medan | Sumatera Utara |
| CAB-02 | Padang | Sumatera Barat |
| CAB-03 | Palembang | Sumatera Selatan |
| CAB-04 | Jakarta | DKI Jakarta |
| CAB-05 | Bandung | Jawa Barat |
| CAB-06 | Semarang | Jawa Tengah |
| CAB-07 | Surabaya | Jawa Timur |
| CAB-08 | Denpasar | Bali |
| CAB-09 | Makassar | Sulawesi Selatan |
| CAB-10 | Pontianak | Kalimantan Barat |

### B. Mapping 15 Produk

| Kode | Nama Standar | Kategori | Harga Standar |
|------|-------------|----------|---------------|
| MSV-001 | Supralit | Vitamin | Rp 85.000 |
| MSV-002 | Supralit Plus | Vitamin | Rp 125.000 |
| MSV-003 | Vitapoult | Vitamin | Rp 95.000 |
| MSV-004 | Vitamas | Vitamin | Rp 110.000 |
| MSV-005 | Egg Promotor | Vitamin | Rp 135.000 |
| MSV-006 | Masavit | Vitamin | Rp 105.000 |
| MSA-001 | Colimas | Antibiotik | Rp 78.000 |
| MSA-002 | Doxerin Plus | Antibiotik | Rp 119.000 |
| MSA-003 | Enromas | Antibiotik | Rp 92.000 |
| MSA-004 | Moxacol Forte | Antibiotik | Rp 145.000 |
| MSP-001 | Masamix | Premix | Rp 167.000 |
| MSP-002 | Biomas Herbal | Herbal | Rp 155.000 |
| MSX-001 | Coxy-Mas | Antikoksidiosis | Rp 88.000 |
| MSX-002 | GlutaMas | Desinfektan | Rp 97.000 |
| MSX-003 | Septocid | Desinfektan | Rp 72.000 |

---

**Catatan:** Laporan ini dihasilkan dari data simulasi untuk keperluan Data Analyst Test. Visualisasi lengkap tersedia di file `Analisis_Bulanan.ipynb` dan dashboard interaktif di `dashboard.py`.
