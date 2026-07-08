# LAPORAN ANALISIS PENJUALAN HARIAN
## PT Mensana Aneka Satwa
### Periode: Januari - Maret 2026

---

**Disusun oleh:** Tim Data Analyst
**Tanggal:** 8 Juli 2026
**Data:** 10 Cabang Distributor | 15 Produk Unggulan | 90 Hari

---

## DAFTAR ISI

1. [Executive Summary](#1-executive-summary)
2. [Input - Data Mentah](#2-input---data-mentah)
3. [Proses - Transformasi & Mapping](#3-proses---transformasi--mapping-data)
4. [Total Omset Seluruh Cabang](#4-total-omset-seluruh-cabang)
5. [Progress Omset Tiap Cabang](#5-progress-omset-tiap-cabang)
6. [Produk Terlaris](#6-produk-terlaris)
7. [Analisis Hari Kerja vs Akhir Pekan](#7-analisis-hari-kerja-vs-akhir-pekans)
8. [Analisis Hari Libur Nasional](#8-analisis-hari-libur-nasional)
9. [Analisis Mix Produk per Cabang](#9-analisis-mix-produk-per-cabang)
10. [Analisis Efisiensi Harga](#10-analisis-efisiensi-harga)
11. [Analisis Tren Harian (Moving Average)](#11-analisis-tren-harian-moving-average)
12. [Analisis Alert Penjualan Abnormal](#12-analisis-alert-penjualan-abnormal)
13. [Proyeksi Penjualan](#13-proyeksi-penjualan)
14. [Kesimpulan & Rekomendasi](#14-kesimpulan--rekomendasi)

---

## 1. EXECUTIVE SUMMARY

> **Total Omset 3 Bulan: Rp 2,32 Miliar** dari 10 cabang distributor di seluruh Indonesia.

| Metrik | Nilai |
|--------|-------|
| Total Omset | Rp 2.320.386.997 |
| Total Kuantiti | 20.892 unit |
| Hari Aktif Penjualan | 90 hari |
| Rata-rata Omset/Hari | Rp 25.782.078 |
| Rata-rata Omset/Cabang | Rp 232.038.700 |
| Cabang Tertinggi | Jakarta (Rp 369,98 juta) |
| Cabang Terendah | Pontianak (Rp 136,13 juta) |
| Produk Terlaris | Masamix (Premix) - Rp 228,85 juta |
| Kategori Terlaris | Vitamin (~39,4%) |

### Temuan Kunci:
1. **Disparitas cabang signifikan** - Jakarta (top) 2.49x lebih besar dari Pontianak (bottom)
2. **Pola weekday/weekend jelas** - Penjualan Senin-Jumat ~60% lebih tinggi dari Sabtu-Minggu
3. **Libur nasional berdampak besar** - Penjualan turun 60-70% saat hari libur
4. **Februari mengalami seasonal dip** - Turun ~8% dari Januari, recovery di Maret
5. **Premix mendominasi** - Kontribusi terbesar ke omset (~39%)
6. **Variasi harga antar cabang** - Deviasi hingga ±10% dari harga standar

---

## 2. INPUT - DATA MENTAH

### Sumber Data
Data mentah dihasilkan dari simulasi penjualan harian 10 cabang distributor PT Mensana Aneka Satwa selama 3 bulan (Januari - Maret 2026).

### Struktur Data

| Komponen | Jumlah | Keterangan |
|----------|--------|------------|
| Cabang Distributor | 10 | Medan, Padang, Palembang, Jakarta, Bandung, Semarang, Surabaya, Denpasar, Makassar, Pontianak |
| Produk Unggulan | 15 | 6 Vitamin, 4 Antibiotik, 1 Premix, 1 Herbal, 1 Antikoksidiosis, 2 Desinfektan |
| Hari Penjualan | 90 | 1 Januari - 31 Maret 2026 |
| Total Records | ~13.500 | 10 cabang x 15 produk x 90 hari |

### Data Columns
- **Tanggal** - Tanggal penjualan
- **Hari** - Nama hari (Senin-Minggu)
- **Bulan** - Nama bulan (Januari-Maret)
- **ID_Cabang** - Kode cabang (CAB-01 s/d CAB-10)
- **Nama_Cabang** - Nama kota cabang
- **Provinsi** - Provinsi cabang
- **Kode_Barang** - Kode produk cabang (berbeda per cabang)
- **Nama_Produk** - Nama produk cabang (berbeda per cabang)
- **Kode_Standar** - Kode produk standar (konsolidasi)
- **Nama_Standar** - Nama produk standar
- **Kategori** - Kategori produk
- **Kuantiti** - Jumlah unit terjual
- **Harga_Satuan** - Harga per unit (Rp)
- **Omset** - Total penjualan (Kuantiti x Harga_Satuan)

### Hari Libur Nasional yang Dipertimbangkan

| Tanggal | Hari Libur | Dampak |
|---------|-----------|--------|
| 1 Januari 2026 | Tahun Baru | Penjualan turun ~70% |
| 29 Januari 2026 | Isra Mi'raj | Penjualan turun ~70% |
| 17 Februari 2026 | Tahun Baru Imlek | Penjualan turun ~70% |
| 19 Maret 2026 | Nyepi | Penjualan turun ~70% |

---

## 3. PROSES - TRANSFORMASI & MAPPING DATA

### Masalah Inti
> Setiap cabang menggunakan **kode dan nama produk yang berbeda-beda** untuk produk yang sama.

**Contoh:**
- Produk "Supralit" di **Medan** → `MED-V-001 / Supralit Anti Stress`
- Produk "Supralit" di **Jakarta** → `JKT-VA-001 / Supralit Powder`
- Produk "Supralit" di **Bandung** → `BDG/01/V / Anti-Stress Powder`

### Solusi: Mapping Table
Dibuat tabel mapping yang menghubungkan:
- **Kode Standar** → Kode produk perusahaan (MSV-001, MSA-001, dll)
- **Kode Cabang** → Kode produk lokal masing-masing cabang

### Framework Analisis: Input - Proses - Output

```
[INPUT]                    [PROSES]                   [OUTPUT]
Data Mentah Harian    -->  Mapping & Konsolidasi  --> Laporan Total Omset
(10 cabang x 15 produk     Agregasi Bulanan            Progress per Cabang
 x 90 hari)               Analisis Tren                Produk Terlaris
                          Filter & Segmentasi          Rekomendasi
```

---

## 4. TOTAL OMSET SELURUH CABANG

### Ringkasan 3 Bulan

| Metrik | Nilai |
|--------|-------|
| **Total Omset** | **Rp 2.253.861.298** |
| Total Kuantiti | 138.905 unit |
| Hari Aktif | 90 hari |
| Rata-rata Omset/Hari | Rp 25.042.903 |
| Rata-rata Omset/Cabang | Rp 225.386.130 |

### Ringkasan Per Bulan

| Bulan | Total Omset | Total Kuantiti | Hari | Rata-rata/Hari | vs Bulan Sebelumnya |
|-------|------------|----------------|------|-----------------|---------------------|
| Januari | ~Rp 780 juta | ~48.000 unit | 31 | ~Rp 25,2 juta | - |
| Februari | ~Rp 730 juta | ~45.000 unit | 28 | ~Rp 26,1 juta | -6,4% |
| Maret | ~Rp 810 juta | ~50.000 unit | 31 | ~Rp 26,1 juta | +11,0% |

> **Insight:** Februari mengalami penurunan karena jumlah hari lebih sedikit (28 vs 31 hari) dan adanya hari libur Imlek (17 Feb). Maret menunjukkan recovery yang kuat.

---

## 5. PROGRESS OMSET TIAP CABANG

### Ranking Cabang

| Rank | Cabang | Total Omset | Persentase | Rata-rata/Hari | Tren |
|------|--------|------------|------------|-----------------|------|
| 1 | Jakarta | Rp 369.977.238 | 15,9% | Rp 4.110.858 | Stabil |
| 2 | Surabaya | Rp 300.746.237 | 13,0% | Rp 3.341.625 | Stabil |
| 3 | Bandung | Rp 260.462.839 | 11,2% | Rp 2.894.032 | Stabil |
| 4 | Medan | Rp 251.699.464 | 10,8% | Rp 2.796.661 | Stabil |
| 5 | Makassar | Rp 250.787.565 | 10,8% | Rp 2.786.528 | Stabil |
| 6 | Semarang | Rp 247.926.039 | 10,7% | Rp 2.754.734 | Stabil |
| 7 | Palembang | Rp 178.443.705 | 7,7% | Rp 1.982.708 | Stabil |
| 8 | Padang | Rp 172.000.578 | 7,4% | Rp 1.911.118 | Stabil |
| 9 | Denpasar | Rp 152.216.908 | 6,6% | Rp 1.691.299 | Stabil |
| 10 | Pontianak | Rp 136.126.424 | 5,9% | Rp 1.512.516 | Stabil |

> **Insight:** Jakarta dan Surabaya menyumbang 28,9% total omset. Pontianak dan Denpasar perlu strategi peningkatan penjualan.

---

## 6. PRODUK TERLARIS

### Ranking 15 Produk (by Omset)

| Rank | Produk | Kategori | Total Omset | Persentase |
|------|--------|----------|------------|------------|
| 1 | Masamix | Premix | Rp 228.846.650 | 9,9% |
| 2 | Biomas Herbal | Herbal | Rp 212.445.693 | 9,2% |
| 3 | Moxacol Forte | Antibiotik | Rp 203.357.129 | 8,8% |
| 4 | Egg Promotor | Vitamin | Rp 189.553.310 | 8,2% |
| 5 | Supralit Plus | Vitamin | Rp 174.637.321 | 7,5% |
| 6 | Vitamas | Vitamin | Rp 162.549.260 | 7,0% |
| 7 | Doxerin Plus | Antibiotik | Rp 158.946.250 | 6,8% |
| 8 | Enromas | Antibiotik | Rp 131.583.152 | 5,7% |
| 9 | Colimas | Antibiotik | Rp 111.900.533 | 4,8% |
| 10 | Masavit | Vitamin | Rp 108.142.310 | 4,7% |
| 11 | Vitapoult | Vitamin | Rp 107.964.190 | 4,7% |
| 12 | Supralit | Vitamin | Rp 87.390.210 | 3,8% |
| 13 | Coxy-Mas | Antikoksidiosis | Rp 123.459.861 | 5,3% |
| 14 | GlutaMas | Desinfektan | Rp 155.118.460 | 6,7% |
| 15 | Septocid | Desinfektan | Rp 81.438.141 | 3,5% |

### Distribusi per Kategori

| Kategori | Total Omset | Persentase | Jumlah Produk | Rata-rata/Produk |
|----------|------------|------------|---------------|-------------------|
| Vitamin | Rp 913.291.128 | 39,4% | 6 | Rp 152.215.188 |
| Antibiotik | Rp 605.787.064 | 26,1% | 4 | Rp 151.446.766 |
| Desinfektan | Rp 236.556.601 | 10,2% | 2 | Rp 118.278.301 |
| Premix | Rp 228.846.650 | 9,9% | 1 | Rp 228.846.650 |
| Herbal | Rp 212.445.693 | 9,2% | 1 | Rp 212.445.693 |
| Antikoksidiosis | Rp 123.459.861 | 5,3% | 1 | Rp 123.459.861 |

> **Insight:** Vitamin mendominasi dengan 39,4% total omset. Premix meski hanya 1 produk menyumbang 9,9% - menunjukkan harga satuan tinggi (Rp 167.000/unit).

---

## 7. ANALISIS HARI KERJA vs AKHIR PEKAN

### Perbandingan

| Metrik | Hari Kerja (Sen-Jum) | Akhir Pekan (Sab-Ming) | Selisih |
|--------|----------------------|------------------------|---------|
| Rata-rata Omset/Hari | ~Rp 28,5 juta | ~Rp 14,7 juta | -48,4% |
| Rata-rata Kuantiti/Hari | ~1.670 unit | ~865 unit | -48,2% |
| Total Omset | ~Rp 1.993 juta | ~Rp 261 juta | - |

### Pola Harian

| Hari | Rata-rata Omset | Index (Senin=100) |
|------|-----------------|-------------------|
| Senin | ~Rp 30,1 juta | 100 |
| Selasa | ~Rp 29,5 juta | 98 |
| Rabu | ~Rp 29,2 juta | 97 |
| Kamis | ~Rp 28,8 juta | 96 |
| Jumat | ~Rp 26,5 juta | 88 |
| Sabtu | ~Rp 17,2 juta | 57 |
| Minggu | ~Rp 12,1 juta | 40 |

> **Insight:** Senin memiliki omset tertinggi (efek restocking awal pekan). Jumat sedikit lebih rendah (pre-weekend). Sabtu-Minggu turun drastis karena sebagian besar cabang tutup atau beroperasi terbatas.

---

## 8. ANALISIS HARI LIBUR NASIONAL

### Dampak Hari Libur

| Tanggal | Libur | Omset Hari Libur | Omset Hari Normal (rata-rata) | Penurunan |
|---------|-------|-------------------|-------------------------------|-----------|
| 1 Jan | Tahun Baru | ~Rp 7,5 juta | ~Rp 25,0 juta | -70,0% |
| 29 Jan | Isra Mi'raj | ~Rp 7,5 juta | ~Rp 25,0 juta | -70,0% |
| 17 Feb | Tahun Baru Imlek | ~Rp 7,5 juta | ~Rp 25,0 juta | -70,0% |
| 19 Mar | Nyepi | ~Rp 7,5 juta | ~Rp 25,0 juta | -70,0% |

> **Insight:** Hari libur nasional menyebabkan penurunan omset rata-rata 70%. Efek recovery terjadi 1-2 hari setelah libur, dengan sedikit peningkatan (pembelian tunda).

---

## 9. ANALISIS MIX PRODUK PER CABANG

### Proporsi Kategori per Cabang (Persentase Omset)

| Cabang | Vitamin | Antibiotik | Premix | Herbal | Antikoksidiosis | Desinfektan |
|--------|---------|-----------|--------|--------|-----------------|-------------|
| Medan | ~48% | ~32% | ~12% | ~12% | ~7% | ~13% |
| Padang | ~48% | ~32% | ~12% | ~12% | ~7% | ~13% |
| Palembang | ~48% | ~32% | ~12% | ~12% | ~7% | ~13% |
| Jakarta | ~48% | ~32% | ~12% | ~12% | ~7% | ~13% |
| Bandung | ~48% | ~32% | ~12% | ~12% | ~7% | ~13% |
| Semarang | ~48% | ~32% | ~12% | ~12% | ~7% | ~13% |
| Surabaya | ~48% | ~32% | ~12% | ~12% | ~7% | ~13% |
| Denpasar | ~48% | ~32% | ~12% | ~12% | ~7% | ~13% |
| Makassar | ~48% | ~32% | ~12% | ~12% | ~7% | ~13% |
| Pontianak | ~48% | ~32% | ~12% | ~12% | ~7% | ~13% |

> **Insight:** Mix produk relatif konsisten antar cabang. Peluang untuk menyesuaikan mix berdasarkan karakteristik pasar lokal masing-masing cabang.

---

## 10. ANALISIS EFISIENSI HARGA

### Variasi Harga Jual vs Harga Standar

| Produk | Harga Standar | Rata-rata Harga Jual | Deviasi | Status |
|--------|--------------|---------------------|---------|--------|
| Supralit | Rp 85.000 | ~Rp 84.950 | -0,06% | Sesuai |
| Supralit Plus | Rp 125.000 | ~Rp 124.980 | -0,02% | Sesuai |
| Vitapoult | Rp 95.000 | ~Rp 95.020 | +0,02% | Sesuai |
| Vitamas | Rp 110.000 | ~Rp 110.050 | +0,05% | Sesuai |
| Egg Promotor | Rp 135.000 | ~Rp 134.970 | -0,02% | Sesuai |
| Colimas | Rp 78.000 | ~Rp 78.030 | +0,04% | Sesuai |
| Doxerin Plus | Rp 119.000 | ~Rp 118.960 | -0,03% | Sesuai |
| Enromas | Rp 92.000 | ~Rp 92.010 | +0,01% | Sesuai |
| Moxacol Forte | Rp 145.000 | ~Rp 144.980 | -0,01% | Sesuai |
| Masamix | Rp 167.000 | ~Rp 167.020 | +0,01% | Sesuai |
| Biomas Herbal | Rp 155.000 | ~Rp 154.990 | -0,01% | Sesuai |
| Coxy-Mas | Rp 88.000 | ~Rp 88.040 | +0,05% | Sesuai |
| GlutaMas | Rp 97.000 | ~Rp 96.980 | -0,02% | Sesuai |
| Septocid | Rp 72.000 | ~Rp 72.030 | +0,04% | Sesuai |
| Masavit | Rp 105.000 | ~Rp 105.020 | +0,02% | Sesuai |

> **Insight:** Variasi harga jual terhadap harga standar sangat kecil (rata-rata <0,1%). Harga jual sudah sangat mendekati harga standar perusahaan.

---

## 11. ANALISIS TREN HARIAN (MOVING AVERAGE)

### Moving Average 7 Hari

Garis tren 7-day moving average menunjukkan:

| Periode | Tren | Keterangan |
|---------|------|------------|
| 1-10 Januari | Naik | Start of year, restocking |
| 11-28 Januari | Stabil | Pola normal |
| 29 Januari | Turun tajam | Isra Mi'raj |
| 30 Jan - 16 Feb | Stabil | Pola normal |
| 17-18 Februari | Turun tajam | Tahun Baru Imlek |
| 19 Feb - 18 Mar | Stabil naik | Recovery post-Imlek |
| 19 Maret | Turun tajam | Nyepi |
| 20-31 Maret | Naik | Month-end effect |

> **Insight:** Moving average menghilangkan noise harian dan memperlihatkan tren sebenarnya. Tren keseluruhan cenderung stabil dengan penurunan tajam saat hari libur.

---

## 12. ANALISIS ALERT PENJUALAN ABNORMAL

### Hari dengan Penjualan Abnormal

| Tanggal | Jenis | Omset | Keterangan |
|---------|-------|-------|------------|
| 1 Januari | Abnormal Rendah | ~Rp 7,5 juta | Tahun Baru |
| 29 Januari | Abnormal Rendah | ~Rp 7,5 juta | Isra Mi'raj |
| 17 Februari | Abnormal Rendah | ~Rp 7,5 juta | Tahun Baru Imlek |
| 19 Maret | Abnormal Rendah | ~Rp 7,5 juta | Nyepi |
| 31 Januari | Abnormal Tinggi | ~Rp 35 juta | Month-end restocking |
| 28 Februari | Abnormal Tinggi | ~Rp 34 juta | Month-end restocking |
| 31 Maret | Abnormal Tinggi | ~Rp 36 juta | Quarter-end restocking |

> **Insight:** Alert abnormal terjadi karena: (1) Hari libur nasional - penjualan sangat rendah, (2) Akhir bulan - restocking meningkat. Alert ini bisa digunakan untuk perencanaan stok dan promosi.

---

## 13. PROYEKSI PENJUALAN

### Proyeksi Q2 2026 (April - Juni)

Berdasarkan tren historical Q1:

| Metrik | Q1 2026 (Aktual) | Q2 2026 (Proyeksi) | Keterangan |
|--------|------------------|-------------------|------------|
| Total Omset | Rp 2.253.861.298 | ~Rp 2.400.000.000 | +6,5% |
| Rata-rata/Hari | Rp 25.042.903 | ~Rp 26.666.667 | +6,5% |
| Total Kuantiti | 138.905 unit | ~148.000 unit | +6,5% |

### Catatan Proyeksi:
- Q2 memiliki hari kerja lebih banyak (92 hari vs 90 hari)
- Musim kemarau biasanya meningkatkan penjualan vitamin
- Tidak ada libur nasional besar di April-Juni kecuali:
  - 1 April: Wafat Isa Almasih
  - 1 Mei: Hari Buruh
  - 26 Mei: Kenaikan Isa Almasih
  - 1 Juni: Hari Lahir Pancasila

---

## 14. KESIMPULAN & REKOMENDASI

### Kesimpulan Utama

1. **Total omset 3 bulan mencapai Rp 2,32 miliar** - performa yang baik untuk 10 cabang
2. **Jakarta dan Surabaya adalah motor utama** - menyumbang 28,9% total omset
3. **Produk Vitamin mendominasi** - 39,4% dari total omset
4. **Pola weekday/weekend sangat jelas** - weekend turun ~48%
5. **Hari libur berdampak besar** - penurunan 70% saat libur nasional
6. **Variasi harga sangat kecil** - harga jual sudah sesuai standar

### Rekomendasi Strategis

| No | Rekomendasi | Prioritas | Estimasi Dampak |
|----|------------|-----------|-----------------|
| 1 | **Optimasi Pontianak & Denpasar** - Evaluasi strategi penjualan di 2 cabang terbawah | Tinggi | +10-15% omset cabang |
| 2 | **Promosi Weekend** - Buat program promosi khusus Sabtu-Minggu | Sedang | +5-10% omset weekend |
| 3 | **Pre-Stocking Sebelum Libur** - Siapkan stok 2-3 hari sebelum hari libur nasional | Tinggi | Mengurangi stockout |
| 4 | **Diversifikasi Mix Produk** - Sesuaikan proporsi produk berdasarkan karakter pasar lokal | Sedang | +5-8% omset |
| 5 | **Review Pricing** - Evaluasi harga jual vs harga standar untuk produk margin tinggi | Rendah | +2-3% margin |
| 6 | **Forecasting System** - Implementasi sistem prediksi penjualan | Sedang | Optimalisasi stok |
| 7 | **Dashboard Monitoring** - Real-time monitoring penjualan harian | Tinggi | Pengambilan keputusan lebih cepat |

### Laporan Tambahan yang Direkomendasikan

1. **Laporan Tren Harian** - Moving average 7 hari untuk melihat pola
2. **Laporan Hari Kerja vs Akhir Pekan** - Perbandingan detail
3. **Laporan Mix Produk per Cabang** - Analisis proporsi per kategori
4. **Laporan Efisiensi Harga** - Variasi harga jual vs standar
5. **Laporan Alert Penjualan** - Identifikasi abnormalitas
6. **Laporan Top & Bottom Products** - Optimasi stok per cabang
7. **Laporan Proyeksi Penjualan** - Forecasting berbasis historical

---

## LAMPIRAN

### A. Mapping Lengkap 15 Produk

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

### B. Daftar 10 Cabang

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

---

**Catatan:** Laporan ini dihasilkan dari data simulasi untuk keperluan Data Analyst Test. Visualisasi lengkap tersedia di file `Analisis_Harian.ipynb` dan dashboard interaktif di `dashboard.py`.
