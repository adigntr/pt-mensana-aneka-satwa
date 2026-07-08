"""
Generate DAILY sales data for 10 PT Mensana Aneka Satwa branches.
3 months (Jan-Mar 2026) x 10 branches x 15 products = ~4,500 records
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

# 10 Branch locations across Indonesia
BRANCHES = [
    {"id": "CAB-01", "name": "Medan", "region": "Sumatera Utara"},
    {"id": "CAB-02", "name": "Padang", "region": "Sumatera Barat"},
    {"id": "CAB-03", "name": "Palembang", "region": "Sumatera Selatan"},
    {"id": "CAB-04", "name": "Jakarta", "region": "DKI Jakarta"},
    {"id": "CAB-05", "name": "Bandung", "region": "Jawa Barat"},
    {"id": "CAB-06", "name": "Semarang", "region": "Jawa Tengah"},
    {"id": "CAB-07", "name": "Surabaya", "region": "Jawa Timur"},
    {"id": "CAB-08", "name": "Denpasar", "region": "Bali"},
    {"id": "CAB-09", "name": "Makassar", "region": "Sulawesi Selatan"},
    {"id": "CAB-10", "name": "Pontianak", "region": "Kalimantan Barat"},
]

# 15 Standard Products (PT Mensana actual products)
STANDARD_PRODUCTS = [
    {"std_code": "MSV-001", "std_name": "Supralit", "category": "Vitamin", "unit_price": 85000},
    {"std_code": "MSV-002", "std_name": "Supralit Plus", "category": "Vitamin", "unit_price": 125000},
    {"std_code": "MSV-003", "std_name": "Vitapoult", "category": "Vitamin", "unit_price": 95000},
    {"std_code": "MSV-004", "std_name": "Vitamas", "category": "Vitamin", "unit_price": 110000},
    {"std_code": "MSV-005", "std_name": "Egg Promotor", "category": "Vitamin", "unit_price": 135000},
    {"std_code": "MSA-001", "std_name": "Colimas", "category": "Antibiotik", "unit_price": 78000},
    {"std_code": "MSA-002", "std_name": "Doxerin Plus", "category": "Antibiotik", "unit_price": 119000},
    {"std_code": "MSA-003", "std_name": "Enromas", "category": "Antibiotik", "unit_price": 92000},
    {"std_code": "MSA-004", "std_name": "Moxacol Forte", "category": "Antibiotik", "unit_price": 145000},
    {"std_code": "MSP-001", "std_name": "Masamix", "category": "Premix", "unit_price": 167000},
    {"std_code": "MSP-002", "std_name": "Biomas Herbal", "category": "Herbal", "unit_price": 155000},
    {"std_code": "MSX-001", "std_name": "Coxy-Mas", "category": "Antikoksidiosis", "unit_price": 88000},
    {"std_code": "MSX-002", "std_name": "GlutaMas", "category": "Desinfektan", "unit_price": 97000},
    {"std_code": "MSX-003", "std_name": "Septocid", "category": "Desinfektan", "unit_price": 72000},
    {"std_code": "MSV-006", "std_name": "Masavit", "category": "Vitamin", "unit_price": 105000},
]

# Branch-specific product codes and names (COMPLETELY DIFFERENT per branch)
BRANCH_PRODUCTS = {
    "CAB-01": [  # Medan - uses "MED" prefix
        {"branch_code": "MED-V-001", "branch_name": "Supralit Anti Stress"},
        {"branch_code": "MED-V-002", "branch_name": "Supralit+"},
        {"branch_code": "MED-V-003", "branch_name": "Vita Broiler"},
        {"branch_code": "MED-V-004", "branch_name": "Vitamin 13"},
        {"branch_code": "MED-V-005", "branch_name": "Egg Booster"},
        {"branch_code": "MED-A-001", "branch_name": "Coli Medicine"},
        {"branch_code": "MED-A-002", "branch_name": "Doxycillin Plus"},
        {"branch_code": "MED-A-003", "branch_name": "Enro 10%"},
        {"branch_code": "MED-A-004", "branch_name": "Amox Forte"},
        {"branch_code": "MED-P-001", "branch_name": "Premix Layer"},
        {"branch_code": "MED-P-002", "branch_name": "Herbal Ternak"},
        {"branch_code": "MED-X-001", "branch_name": "Anti Coccid"},
        {"branch_code": "MED-X-002", "branch_name": "Desinfek 100"},
        {"branch_code": "MED-X-003", "branch_name": "Iodine 2%"},
        {"branch_code": "MED-V-006", "branch_name": "Multi Vitamin"},
    ],
    "CAB-02": [  # Padang - uses "PDG" prefix
        {"branch_code": "PDG-001A", "branch_name": "Stress Relief"},
        {"branch_code": "PDG-002A", "branch_name": "Vitamin Plus Stress"},
        {"branch_code": "PDG-003A", "branch_name": "Growth Vit"},
        {"branch_code": "PDG-004A", "branch_name": "Vit 13 Komplit"},
        {"branch_code": "PDG-005A", "branch_name": "Telur Max"},
        {"branch_code": "PDG-006A", "branch_name": "Obat E-Coli"},
        {"branch_code": "PDG-007A", "branch_name": "CRD Medicine"},
        {"branch_code": "PDG-008A", "branch_name": "Fluoro 100"},
        {"branch_code": "PDG-009A", "branch_name": "Amoxicillin 200"},
        {"branch_code": "PDG-010A", "branch_name": "Pakan Premix"},
        {"branch_code": "PDG-011A", "branch_name": "Jamu Ternak"},
        {"branch_code": "PDG-012A", "branch_name": "Coccid Guard"},
        {"branch_code": "PDG-013A", "branch_name": "Kandang Clean"},
        {"branch_code": "PDG-014A", "branch_name": "Betadine Hewan"},
        {"branch_code": "PDG-015A", "branch_name": "Vitamin Ternak"},
    ],
    "CAB-03": [  # Palembang - uses "PLB" prefix
        {"branch_code": "PLB.V.001", "branch_name": "Anti Stress Cap"},
        {"branch_code": "PLB.V.002", "branch_name": "Vitamin Stress+"},
        {"branch_code": "PLB.V.003", "branch_name": "Pedaging Vit"},
        {"branch_code": "PLB.V.004", "branch_name": "Thirteen Vit"},
        {"branch_code": "PLB.V.005", "branch_name": "Producer Egg"},
        {"branch_code": "PLB.A.001", "branch_name": "Trimethoprim-Sulfa"},
        {"branch_code": "PLB.A.002", "branch_name": "Doxycycline Forte"},
        {"branch_code": "PLB.A.003", "branch_name": "Enrofloxacin 10"},
        {"branch_code": "PLB.A.004", "branch_name": "Amoxicillin High"},
        {"branch_code": "PLB.P.001", "branch_name": "Mix Pakan"},
        {"branch_code": "PLB.P.002", "branch_name": "Ekstrak Herbal"},
        {"branch_code": "PLB.X.001", "branch_name": "Diclazuril Mix"},
        {"branch_code": "PLB.X.002", "branch_name": "Glutaral Fix"},
        {"branch_code": "PLB.X.003", "branch_name": "Povidone Wash"},
        {"branch_code": "PLB.V.006", "branch_name": "A-D-E Vitamin"},
    ],
    "CAB-04": [  # Jakarta - uses "JKT" prefix
        {"branch_code": "JKT-VA-001", "branch_name": "Supralit Powder"},
        {"branch_code": "JKT-VA-002", "branch_name": "Supralit Liquid+"},
        {"branch_code": "JKT-VA-003", "branch_name": "Vita Grow Bro"},
        {"branch_code": "JKT-VA-004", "branch_name": "Multi Vit 13"},
        {"branch_code": "JKT-VA-005", "branch_name": "Egg Production+"},
        {"branch_code": "JKT-AB-001", "branch_name": "Coli Ban"},
        {"branch_code": "JKT-AB-002", "branch_name": "Doxerin Syrup"},
        {"branch_code": "JKT-AB-003", "branch_name": "Enromas Liquid"},
        {"branch_code": "JKT-AB-004", "branch_name": "Amox Forte 200"},
        {"branch_code": "JKT-PR-001", "branch_name": "Premix Pro"},
        {"branch_code": "JKT-PR-002", "branch_name": "Herbal Mas"},
        {"branch_code": "JKT-AN-001", "branch_name": "Coxy Stop"},
        {"branch_code": "JKT-AN-002", "branch_name": "Desinfect Pro"},
        {"branch_code": "JKT-AN-003", "branch_name": "Iodine Scrub"},
        {"branch_code": "JKT-VA-006", "branch_name": "Vita Complete"},
    ],
    "CAB-05": [  # Bandung - uses "BDG" prefix
        {"branch_code": "BDG/01/V", "branch_name": "Anti-Stress Powder"},
        {"branch_code": "BDG/02/V", "branch_name": "Stress-Vit Plus"},
        {"branch_code": "BDG/03/V", "branch_name": "Broiler Vita"},
        {"branch_code": "BDG/04/V", "branch_name": "Vitamin Lengkap"},
        {"branch_code": "BDG/05/V", "branch_name": "Egg Power"},
        {"branch_code": "BDG/01/A", "branch_name": "E-Coli Block"},
        {"branch_code": "BDG/02/A", "branch_name": "Doxycycline Mix"},
        {"branch_code": "BDG/03/A", "branch_name": "Enrofloxacin Pro"},
        {"branch_code": "BDG/04/A", "branch_name": "Amox Plus"},
        {"branch_code": "BDG/01/P", "branch_name": "Nutri Premix"},
        {"branch_code": "BDG/02/P", "branch_name": "Herbal Extract"},
        {"branch_code": "BDG/01/X", "branch_name": "Coccid Shield"},
        {"branch_code": "BDG/02/X", "branch_name": "Kandang Sanit"},
        {"branch_code": "BDG/03/X", "branch_name": "Iodine Solution"},
        {"branch_code": "BDG/06/V", "branch_name": "Complete Vit"},
    ],
    "CAB-06": [  # Semarang - uses "SMG" prefix
        {"branch_code": "SMG-V-101", "branch_name": "StressGuard"},
        {"branch_code": "SMG-V-102", "branch_name": "VitaGuard Plus"},
        {"branch_code": "SMG-V-103", "branch_name": "GrowthVit Bro"},
        {"branch_code": "SMG-V-104", "branch_name": "VitaMix 13"},
        {"branch_code": "SMG-V-105", "branch_name": "EggVita Pro"},
        {"branch_code": "SMG-A-101", "branch_name": "ColiClear"},
        {"branch_code": "SMG-A-102", "branch_name": "DoxiCure"},
        {"branch_code": "SMG-A-103", "branch_name": "EnroCure 10"},
        {"branch_code": "SMG-A-104", "branch_name": "AmoxiMax"},
        {"branch_code": "SMG-P-101", "branch_name": "Premix Complete"},
        {"branch_code": "SMG-P-102", "branch_name": "HerbalMax"},
        {"branch_code": "SMG-X-101", "branch_name": "CoxyGuard"},
        {"branch_code": "SMG-X-102", "branch_name": "SanitMax"},
        {"branch_code": "SMG-X-103", "branch_name": "IodineMax"},
        {"branch_code": "SMG-V-106", "branch_name": "VitaMax All"},
    ],
    "CAB-07": [  # Surabaya - uses "SBY" prefix
        {"branch_code": "SBY#V01", "branch_name": "AntiStress SBY"},
        {"branch_code": "SBY#V02", "branch_name": "Vit Stress Pro"},
        {"branch_code": "SBY#V03", "branch_name": "PedagingVit SBY"},
        {"branch_code": "SBY#V04", "branch_name": "13 Vitamin SBY"},
        {"branch_code": "SBY#V05", "branch_name": "Egg Max SBY"},
        {"branch_code": "SBY#A01", "branch_name": "Colimas SBY"},
        {"branch_code": "SBY#A02", "branch_name": "Doxerin SBY"},
        {"branch_code": "SBY#A03", "branch_name": "Enromas SBY"},
        {"branch_code": "SBY#A04", "branch_name": "Amox SBY"},
        {"branch_code": "SBY#P01", "branch_name": "Premix SBY"},
        {"branch_code": "SBY#P02", "branch_name": "Herbal SBY"},
        {"branch_code": "SBY#X01", "branch_name": "Coxy SBY"},
        {"branch_code": "SBY#X02", "branch_name": "Desinfek SBY"},
        {"branch_code": "SBY#X03", "branch_name": "Iodine SBY"},
        {"branch_code": "SBY#V06", "branch_name": "MultiVit SBY"},
    ],
    "CAB-08": [  # Denpasar - uses "DPS" prefix
        {"branch_code": "DPS-V001", "branch_name": "Stress Free"},
        {"branch_code": "DPS-V002", "branch_name": "Vitamin Free+"},
        {"branch_code": "DPS-V003", "branch_name": "GrowVit DPS"},
        {"branch_code": "DPS-V004", "branch_name": "Vit Complete"},
        {"branch_code": "DPS-V005", "branch_name": "Egg Force"},
        {"branch_code": "DPS-A001", "branch_name": "Coli Force"},
        {"branch_code": "DPS-A002", "branch_name": "Doxi Force"},
        {"branch_code": "DPS-A003", "branch_name": "Enro Force"},
        {"branch_code": "DPS-A004", "branch_name": "Amox Force"},
        {"branch_code": "DPS-P001", "branch_name": "Premix Force"},
        {"branch_code": "DPS-P002", "branch_name": "Herbal Force"},
        {"branch_code": "DPS-X001", "branch_name": "Coxy Force"},
        {"branch_code": "DPS-X002", "branch_name": "Sanit Force"},
        {"branch_code": "DPS-X003", "branch_name": "Iodine Force"},
        {"branch_code": "DPS-V006", "branch_name": "MultiForce"},
    ],
    "CAB-09": [  # Makassar - uses "MKS" prefix
        {"branch_code": "MKS.V.01", "branch_name": "AntiStress MKS"},
        {"branch_code": "MKS.V.02", "branch_name": "StressRelief+"},
        {"branch_code": "MKS.V.03", "branch_name": "Growth Pro MKS"},
        {"branch_code": "MKS.V.04", "branch_name": "Vitamin Pro 13"},
        {"branch_code": "MKS.V.05", "branch_name": "Egg Pro MKS"},
        {"branch_code": "MKS.A.01", "branch_name": "Coli Pro MKS"},
        {"branch_code": "MKS.A.02", "branch_name": "Doxi Pro MKS"},
        {"branch_code": "MKS.A.03", "branch_name": "Enro Pro MKS"},
        {"branch_code": "MKS.A.04", "branch_name": "Amox Pro MKS"},
        {"branch_code": "MKS.P.01", "branch_name": "Premix Pro MKS"},
        {"branch_code": "MKS.P.02", "branch_name": "Herbal Pro MKS"},
        {"branch_code": "MKS.X.01", "branch_name": "Coxy Pro MKS"},
        {"branch_code": "MKS.X.02", "branch_name": "Sanit Pro MKS"},
        {"branch_code": "MKS.X.03", "branch_name": "Iodine Pro MKS"},
        {"branch_code": "MKS.V.06", "branch_name": "MultiVit Pro"},
    ],
    "CAB-10": [  # Pontianak - uses "PNK" prefix
        {"branch_code": "PNK~V~01", "branch_name": "StressNo More"},
        {"branch_code": "PNK~V~02", "branch_name": "VitNo Stress+"},
        {"branch_code": "PNK~V~03", "branch_name": "Bro Grow"},
        {"branch_code": "PNK~V~04", "branch_name": "Vitamin 13 All"},
        {"branch_code": "PNK~V~05", "branch_name": "Egg Boost"},
        {"branch_code": "PNK~A~01", "branch_name": "ColiBlock"},
        {"branch_code": "PNK~A~02", "branch_name": "DoxiBlock"},
        {"branch_code": "PNK~A~03", "branch_name": "EnroBlock"},
        {"branch_code": "PNK~A~04", "branch_name": "AmoxBlock"},
        {"branch_code": "PNK~P~01", "branch_name": "PremixBlock"},
        {"branch_code": "PNK~P~02", "branch_name": "HerbalBlock"},
        {"branch_code": "PNK~X~01", "branch_name": "CoxyBlock"},
        {"branch_code": "PNK~X~02", "branch_name": "SanitBlock"},
        {"branch_code": "PNK~X~03", "branch_name": "IodineBlock"},
        {"branch_code": "PNK~V~06", "branch_name": "MultiBlock"},
    ],
}

# Generate date range for 3 months
start_date = datetime(2026, 1, 1)
end_date = datetime(2026, 3, 31)
date_range = pd.date_range(start=start_date, end=end_date, freq='D')

# Indonesian day names
DAY_NAMES = {
    0: 'Senin', 1: 'Selasa', 2: 'Rabu', 3: 'Kamis',
    4: 'Jumat', 5: 'Sabtu', 6: 'Minggu'
}

# Month names in Indonesian
MONTH_NAMES = {1: 'Januari', 2: 'Februari', 3: 'Maret'}


def generate_daily_data():
    """Generate realistic daily sales data for 10 branches x 15 products x 90 days."""
    all_data = []

    # City demand multiplier (larger cities = higher sales)
    city_multiplier = {
        "CAB-01": 1.2, "CAB-02": 0.8, "CAB-03": 0.9,
        "CAB-04": 1.5, "CAB-05": 1.3, "CAB-06": 1.1,
        "CAB-07": 1.4, "CAB-08": 0.7, "CAB-09": 1.0, "CAB-10": 0.6,
    }

    # Product demand patterns (some products sell more on certain days)
    product_daily_factor = {
        'Vitamin': lambda day: 1.0 + 0.05 * np.sin(day * np.pi / 7),  # Weekly cycle
        'Antibiotik': lambda day: 1.0 + 0.075 * np.cos(day * np.pi / 14),  # Bi-weekly
        'Premix': lambda day: 1.0 + 0.025 * np.sin(day * np.pi / 30),  # Monthly cycle
        'Herbal': lambda day: 1.0 + 0.04 * np.sin(day * np.pi / 21),  # 3-week cycle
        'Antikoksidiosis': lambda day: 1.0 + 0.06 * np.cos(day * np.pi / 10),  # 10-day cycle
        'Desinfektan': lambda day: 1.0 + 0.1 * np.sin(day * np.pi / 14),  # Bi-weekly
    }

    for branch in BRANCHES:
        branch_id = branch["id"]
        branch_products = BRANCH_PRODUCTS[branch_id]
        multiplier = city_multiplier[branch_id]

        for day_idx, date in enumerate(date_range):
            day_of_week = date.dayofweek
            day_name = DAY_NAMES[day_of_week]
            month_name = MONTH_NAMES[date.month]

            # Weekend effect (lower sales on Saturday/Sunday)
            weekend_factor = 0.6 if day_of_week >= 5 else 1.0

            # Holiday effect (lower sales on specific dates)
            holiday_dates = [
                datetime(2026, 1, 1),    # Tahun Baru
                datetime(2026, 1, 29),   # Isra Mi'raj
                datetime(2026, 2, 17),   # Tahun Baru Imlek
                datetime(2026, 3, 19),   # Nyepi
            ]
            holiday_factor = 0.3 if date in holiday_dates else 1.0

            # Monday restocking boost, Friday pre-weekend dip
            if day_of_week == 0:  # Monday
                dow_factor = 1.08
            elif day_of_week == 4:  # Friday
                dow_factor = 0.92
            elif day_of_week >= 5:  # Weekend (already handled by weekend_factor)
                dow_factor = 1.0
            else:
                dow_factor = 1.0

            # Month-end effect (higher sales at end of month)
            month_end_factor = 1.3 if date.day >= 25 else 1.0

            # First-of-month boost
            first_days_boost = 1.15 if date.day <= 2 else 1.0

            for prod_idx, (std_prod, br_prod) in enumerate(zip(STANDARD_PRODUCTS, branch_products)):
                # Base quantity with realistic daily variation
                base_qty = int(np.random.poisson(2) * multiplier)

                # Apply daily factors
                daily_factor = product_daily_factor.get(std_prod['category'], lambda x: 1.0)
                base_qty = int(base_qty * daily_factor(day_idx) * weekend_factor * holiday_factor * month_end_factor * dow_factor * first_days_boost)

                # Ensure minimum quantity (some days might have 0 sales)
                if base_qty < 1:
                    # 70% chance of having sales, 30% chance of no sales
                    if np.random.random() < 0.7:
                        base_qty = 1
                    else:
                        base_qty = 0

                # Price variation (±10% from standard)
                price_variation = np.random.uniform(0.9, 1.1)
                unit_price = int(std_prod['unit_price'] * price_variation)

                # Calculate omset (revenue)
                omset = base_qty * unit_price

                all_data.append({
                    'Tanggal': date.strftime('%Y-%m-%d'),
                    'Hari': day_name,
                    'Bulan': month_name,
                    'Tahun': 2026,
                    'ID_Cabang': branch_id,
                    'Nama_Cabang': branch['name'],
                    'Provinsi': branch['region'],
                    'Kode_Barang': br_prod['branch_code'],
                    'Nama_Produk': br_prod['branch_name'],
                    'Kode_Standar': std_prod['std_code'],
                    'Nama_Standar': std_prod['std_name'],
                    'Kategori': std_prod['category'],
                    'Kuantiti': base_qty,
                    'Harga_Satuan': unit_price,
                    'Omset': omset,
                })

    return pd.DataFrame(all_data)


def generate_product_mapping():
    """Generate mapping table showing product equivalence across branches."""
    mapping_data = []

    for std_prod in STANDARD_PRODUCTS:
        row = {
            'Kode_Standar': std_prod['std_code'],
            'Nama_Standar': std_prod['std_name'],
            'Kategori': std_prod['category'],
            'Harga_Standar': std_prod['unit_price'],
        }

        for branch in BRANCHES:
            branch_id = branch['id']
            br_prod = BRANCH_PRODUCTS[branch_id][STANDARD_PRODUCTS.index(std_prod)]
            row[f'{branch_id}_Kode'] = br_prod['branch_code']
            row[f'{branch_id}_Nama'] = br_prod['branch_name']

        mapping_data.append(row)

    return pd.DataFrame(mapping_data)


def main():
    print("=" * 70)
    print("GENERATING DAILY DATA FOR PT MENSANA ANEKA SATWA")
    print("=" * 70)

    # Generate daily sales data
    df_daily = generate_daily_data()
    print(f"\n[1] Daily Sales Data Generated:")
    print(f"    - Total records: {len(df_daily):,}")
    print(f"    - Date range: {df_daily['Tanggal'].min()} to {df_daily['Tanggal'].max()}")
    print(f"    - Days: {df_daily['Tanggal'].nunique()}")
    print(f"    - Branches: {df_daily['ID_Cabang'].nunique()}")
    print(f"    - Products (unique codes): {df_daily['Kode_Barang'].nunique()}")
    print(f"    - Products (standard names): {df_daily['Nama_Standar'].nunique()}")

    # Save to Excel
    output_file = r"C:\Users\Hito\Documents\PT Mensana Aneka Satwa\Data_Mentah_Harian.xlsx"
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Sheet 1: Daily sales data
        df_daily.to_excel(writer, sheet_name='Data_Penjualan_Harian', index=False)

        # Sheet 2: Product mapping
        df_mapping = generate_product_mapping()
        df_mapping.to_excel(writer, sheet_name='Mapping_Produk', index=False)

        # Sheet 3: Daily summary per branch
        daily_summary = df_daily.groupby(['Tanggal', 'ID_Cabang', 'Nama_Cabang']).agg(
            Total_Kuantiti=('Kuantiti', 'sum'),
            Total_Omset=('Omset', 'sum'),
            Jumlah_Produk=('Kode_Barang', 'count')
        ).reset_index()
        daily_summary.to_excel(writer, sheet_name='Ringkasan_Harian', index=False)

        # Sheet 4: Monthly summary
        monthly_summary = df_daily.groupby(['Bulan', 'ID_Cabang', 'Nama_Cabang']).agg(
            Total_Kuantiti=('Kuantiti', 'sum'),
            Total_Omset=('Omset', 'sum'),
            Jumlah_Hari=('Tanggal', 'nunique'),
            Rata_rata_Harian=('Omset', 'mean')
        ).reset_index()
        monthly_summary.to_excel(writer, sheet_name='Ringkasan_Bulanan', index=False)

        # Sheet 5: Category daily summary
        cat_daily = df_daily.groupby(['Tanggal', 'Kategori']).agg(
            Total_Kuantiti=('Kuantiti', 'sum'),
            Total_Omset=('Omset', 'sum')
        ).reset_index()
        cat_daily.to_excel(writer, sheet_name='Ringkasan_Kategori', index=False)

    print(f"\n[2] Excel File Saved: {output_file}")

    # Print summary statistics
    print("\n" + "=" * 70)
    print("RINGKASAN STATISTIK")
    print("=" * 70)

    total_omset = df_daily['Omset'].sum()
    total_qty = df_daily['Kuantiti'].sum()
    active_days = len(df_daily[df_daily['Kuantiti'] > 0]['Tanggal'].unique())

    print(f"\nTotal Omset 3 Bulan     : Rp {total_omset:>15,.0f}")
    print(f"Total Kuantiti          : {total_qty:>15,} unit")
    print(f"Hari Aktif Penjualan    : {active_days:>15} hari")
    print(f"Rata-rata Omset/Hari    : Rp {total_omset/active_days:>15,.0f}")
    print(f"Rata-rata Omset/Cabang  : Rp {total_omset/10:>15,.0f}")

    print("\n" + "-" * 70)
    print("OMSET PER CABANG:")
    print("-" * 70)
    branch_totals = df_daily.groupby('Nama_Cabang')['Omset'].sum().sort_values(ascending=False)
    for name, omset in branch_totals.items():
        print(f"  {name:15s}: Rp {omset:>15,.0f}")

    print("\n" + "-" * 70)
    print("OMSET PER KATEGORI:")
    print("-" * 70)
    cat_totals = df_daily.groupby('Kategori')['Omset'].sum().sort_values(ascending=False)
    for cat, omset in cat_totals.items():
        print(f"  {cat:20s}: Rp {omset:>15,.0f}")

    print("\n" + "-" * 70)
    print("TOP 5 PRODUK TERLARIS:")
    print("-" * 70)
    prod_totals = df_daily.groupby('Nama_Standar')['Omset'].sum().sort_values(ascending=False).head(5)
    for name, omset in prod_totals.items():
        print(f"  {name:20s}: Rp {omset:>15,.0f}")

    print("\n" + "=" * 70)
    print("DONE!")
    print("=" * 70)


if __name__ == "__main__":
    main()
