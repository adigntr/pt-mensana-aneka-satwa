# PT Mensana Aneka Satwa - Analisis Penjualan Bulanan

Analisis penjualan bulanan Q1 2026 (Januari - Maret) untuk 10 cabang distributor PT Mensana Aneka Satwa.

## 📊 Dashboard Streamlit

**[🔗 Live Dashboard](https://pt-mensana-aneka-satwa.streamlit.app/)** - Dashboard interaktif dengan 5 tabs analisis lengkap

## 🎯 Fitur

- **Data Generator** - Generate data penjualan realistis dengan pola Indonesian holidays
- **Notebook Analisis** - 43 cells analisis dengan 12 visualisasi Plotly
- **Dashboard Interaktif** - Streamlit dashboard dengan 5 tabs
- **Laporan Bulanan** - Markdown report siap export ke PPT/PDF

## 📈 Hasil Analisis Q1 2026

| Metrik | Nilai |
|--------|-------|
| Total Omset | Rp 2.320.386.997 |
| Total Kuantiti | 20.892 unit |
| Cabang Tertinggi | Jakarta (Rp 369,98 juta) |
| Produk Terlaris | Masamix - Premix |
| Kategori Terlaris | Vitamin (39,4%) |

### Tren Bulanan

| Bulan | Total Omset | Growth |
|-------|------------|--------|
| Januari | Rp 791.154.480 | - |
| Februari | Rp 703.493.151 | -11,1% |
| Maret | Rp 825.739.366 | +17,4% |

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/adigntr/pt-mensana-aneka-satwa.git
cd pt-mensana-aneka-satwa

# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run streamlit_app.py

# Or run notebook
jupyter notebook Analisis_Bulanan.ipynb
```

## 📁 Struktur File

```
├── generate_daily_data.py      # Data generator
├── Data_Mentah_Harian.xlsx     # Data mentah (13.500 records)
├── Analisis_Bulanan.ipynb      # Notebook analisis bulanan
├── Analisis_Harian.ipynb       # Notebook analisis harian
├── streamlit_app.py            # Streamlit dashboard
├── dashboard.py                # Dashboard (sama dengan streamlit_app.py)
├── Laporan_Bulanan.md          # Laporan markdown
├── charts/                     # Visualisasi PNG
└── requirements.txt            # Python dependencies
```

## 🎨 Visualisasi

Dashboard menyediakan 5 tabs:
1. **Overview** - Total omset, distribusi cabang & kategori, tren harian
2. **Cabang** - Ranking, progress bulanan, heatmap
3. **Produk** - Top/bottom products, mix per cabang, sunburst
4. **Tren Waktu** - Moving average, weekday vs weekend, holiday impact
5. **Analisis Lanjutan** - Efisiensi harga, alert abnormal, proyeksi Q2

## 📊 Data

- **10 Cabang:** Medan, Padang, Palembang, Jakarta, Bandung, Semarang, Surabaya, Denpasar, Makassar, Pontianak
- **15 Produk:** 6 Vitamin, 4 Antibiotik, 1 Premix, 1 Herbal, 1 Antikoksidiosis, 2 Desinfektan
- **90 Hari:** 1 Januari - 31 Maret 2026
- **Hari Libur:** Tahun Baru (1 Jan), Isra Mi'raj (29 Jan), Imlek (17 Feb), Nyepi (19 Mar)

## 🔧 Requirements

- Python 3.8+
- pandas >= 1.5.0
- numpy >= 1.24.0
- plotly >= 5.15.0
- streamlit >= 1.24.0
- openpyxl >= 3.0.10

## 📝 Laporan

Laporan lengkap tersedia di:
- `Laporan_Bulanan.md` - Laporan analisis bulanan (15 bagian)
- `Laporan_Penjualan.md` - Laporan analisis harian

## 🎯 Insight Utama

1. **Februari mengalami penurunan -11,1%** karena hari lebih sedikit (28 vs 31)
2. **Maret recovery kuat +17,4%** - demand tertunda terpenuhi
3. **Jakarta & Surabaya dominasi 28,9%** total omset
4. **Weekend turun 48%** dari hari kerja
5. **Hari libur berdampak besar** - penurunan 45-49%

## 📧 Contact

Developed for PT Mensana Aneka Satwa Data Analyst Test

---

**⭐ Star this repo if you find it helpful!**
