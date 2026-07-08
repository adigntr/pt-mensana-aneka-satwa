"""
Generate semua visualisasi sebagai PNG untuk laporan PDF.
Jalankan: python generate_charts.py
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import timedelta
import os

# ============================================================
# SETUP
# ============================================================
CHART_DIR = 'charts'
os.makedirs(CHART_DIR, exist_ok=True)

COLORS = {
    'primary': '#0F766E', 'primary_light': '#14B8A6',
    'accent_gold': '#F59E0B', 'accent_coral': '#F97316',
    'accent_blue': '#3B82F6', 'accent_rose': '#F43F5E',
}
CHART_COLORS = ['#14B8A6', '#F59E0B', '#3B82F6', '#F97316', '#8B5CF6', '#F43F5E', '#06B6D4', '#84CC16', '#EC4899', '#6366F1']

FONT = dict(family='Arial, sans-serif', size=13, color='#1E293B')
TEMPLATE = dict(
    paper_bgcolor='white', plot_bgcolor='white',
    font=FONT, margin=dict(l=60, r=30, t=50, b=50),
    xaxis=dict(gridcolor='#E2E8F0', zeroline=False),
    yaxis=dict(gridcolor='#E2E8F0', zeroline=False),
)

def save(fig, name, h=500, w=900):
    fig.update_layout(**TEMPLATE, height=h, width=w)
    fig.write_image(f'{CHART_DIR}/{name}.png', scale=2)
    print(f'  Saved: {name}.png')

# ============================================================
# LOAD DATA
# ============================================================
df = pd.read_excel('Data_Mentah_Harian.xlsx', sheet_name='Data_Penjualan_Harian')
df['Tanggal'] = pd.to_datetime(df['Tanggal'])
month_order = ['Januari', 'Februari', 'Maret']
day_order = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
total_omset = df['Omset'].sum()

print('Generating charts...')

# ============================================================
# CHART 1: Omset per Cabang per Bulan (Grouped Bar)
# ============================================================
df_bulanan = df.groupby(['Bulan', 'Nama_Cabang'])['Omset'].sum().reset_index()
df_bulanan['Bulan'] = pd.Categorical(df_bulanan['Bulan'], categories=month_order, ordered=True)
df_bulanan = df_bulanan.sort_values(['Nama_Cabang', 'Bulan'])

fig1 = px.bar(df_bulanan, x='Nama_Cabang', y='Omset', color='Bulan', barmode='group',
              color_discrete_sequence=[COLORS['primary'], COLORS['accent_gold'], COLORS['accent_blue']],
              labels={'Omset': 'Total Omset (Rp)', 'Nama_Cabang': ''})
fig1.update_layout(title=dict(text='Omset per Cabang per Bulan', x=0.01, font=dict(size=15)),
                   legend=dict(orientation='h', y=1.08, x=0.5, xanchor='center'))
save(fig1, '01_omset_cabang_bulanan', 500)

# ============================================================
# CHART 2: Donut Distribusi Cabang
# ============================================================
branch_total = df.groupby('Nama_Cabang')['Omset'].sum().sort_values(ascending=False)
fig2 = px.pie(values=branch_total.values, names=branch_total.index, hole=0.5,
              color_discrete_sequence=CHART_COLORS)
fig2.update_traces(textposition='inside', textinfo='percent+label', textfont_size=11)
fig2.update_layout(title=dict(text='Distribusi Omset per Cabang (Q1 2026)', x=0.01, font=dict(size=15)),
                   showlegend=False, annotations=[dict(text=f'<b>10</b><br>Cabang', x=0.5, y=0.5, font_size=15, showarrow=False)])
save(fig2, '02_donut_cabang', 500)

# ============================================================
# CHART 3: Top 10 Produk Terlaris
# ============================================================
product_ranking = df.groupby(['Nama_Standar', 'Kategori']).agg(
    Total_Omset=('Omset', 'sum')).reset_index().sort_values('Total_Omset', ascending=False).head(10)

cat_map = dict(zip(product_ranking['Kategori'].unique(), CHART_COLORS[:len(product_ranking['Kategori'].unique())]))
fig3 = px.bar(product_ranking, x='Total_Omset', y='Nama_Standar', color='Kategori',
              orientation='h', color_discrete_map=cat_map,
              labels={'Total_Omset': 'Total Omset (Rp)', 'Nama_Standar': ''})
fig3.update_traces(texttemplate='Rp %{x:,.0f}', textposition='outside', textfont_size=10)
fig3.update_layout(title=dict(text='Top 10 Produk Terlaris (by Omset)', x=0.01, font=dict(size=15)),
                   yaxis=dict(categoryorder='total ascending'), margin=dict(r=120))
save(fig3, '03_top10_produk', 450)

# ============================================================
# CHART 4: Distribusi Kategori (Horizontal Bar)
# ============================================================
cat_bar = df.groupby('Kategori')['Omset'].sum().sort_values(ascending=True).reset_index()
cat_bar.columns = ['Kategori', 'Total_Omset']
cat_bar_colors = [COLORS['accent_blue'], COLORS['accent_coral'], COLORS['accent_gold'],
                  COLORS['accent_rose'], '#8B5CF6', COLORS['primary']][:len(cat_bar)]
fig4 = px.bar(cat_bar, x='Total_Omset', y='Kategori', orientation='h',
              labels={'Total_Omset': 'Total Omset (Rp)', 'Kategori': ''})
fig4.update_traces(marker_color=cat_bar_colors, texttemplate='Rp %{x:,.0f}', textposition='outside', textfont_size=11)
fig4.update_layout(title=dict(text='Total Omset per Kategori', x=0.01, font=dict(size=15)), margin=dict(r=120))
save(fig4, '04_kategori_bar', 400)

# ============================================================
# CHART 5: Tren Harian + Regresi
# ============================================================
daily = df.groupby('Tanggal')['Omset'].sum().reset_index()
daily['day_num'] = (daily['Tanggal'] - daily['Tanggal'].min()).dt.days
coeffs = np.polyfit(daily['day_num'], daily['Omset'], 1)
trend_fn = np.poly1d(coeffs)
daily['Trendline'] = trend_fn(daily['day_num'])

fig5 = go.Figure()
fig5.add_trace(go.Scatter(x=daily['Tanggal'], y=daily['Omset'], mode='lines',
                          name='Omset Harian', line=dict(color=COLORS['primary'], width=1.5),
                          fill='tozeroy', fillcolor='rgba(20,184,166,0.08)'))
fig5.add_trace(go.Scatter(x=daily['Tanggal'], y=daily['Trendline'], mode='lines',
                          name='Trendline Regresi', line=dict(color=COLORS['accent_rose'], width=2.5, dash='dash')))
fig5.update_layout(title=dict(text='Tren Omset Harian dengan Garis Regresi', x=0.01, font=dict(size=15)),
                   xaxis_title='', yaxis_title='Omset (Rp)', legend=dict(orientation='h', y=1.08, x=0.5, xanchor='center'))
save(fig5, '05_tren_harian', 420)

# ============================================================
# CHART 6: Hari Kerja vs Akhir Pekan
# ============================================================
df['Tipe_Hari'] = df['Hari'].apply(lambda x: 'Akhir Pekan' if x in ['Sabtu', 'Minggu'] else 'Hari Kerja')
dow_compare = df.groupby('Tipe_Hari')['Omset'].mean().reset_index()
dow_compare.columns = ['Tipe_Hari', 'Rata_rata']

fig6 = px.bar(dow_compare, x='Tipe_Hari', y='Rata_rata', color='Tipe_Hari',
              color_discrete_map={'Hari Kerja': COLORS['primary'], 'Akhir Pekan': COLORS['accent_coral']},
              labels={'Rata_rata': 'Rata-rata Omset (Rp)', 'Tipe_Hari': ''})
fig6.update_traces(texttemplate='Rp %{y:,.0f}', textposition='outside', textfont_size=11)
fig6.update_layout(title=dict(text='Hari Kerja vs Akhir Pekan', x=0.01, font=dict(size=15)), showlegend=False, yaxis=dict(zeroline=False))
save(fig6, '06_hari_kerja_weekend', 400)

# ============================================================
# CHART 7: Omset per Hari dalam Seminggu
# ============================================================
dow_daily = df.groupby('Hari')['Omset'].sum().reindex(day_order).reset_index()
dow_colors = [COLORS['primary']] * 5 + [COLORS['accent_coral']] * 2

fig7 = px.bar(dow_daily, x='Hari', y='Omset', labels={'Omset': 'Total Omset (Rp)', 'Hari': ''})
fig7.update_traces(marker_color=dow_colors, texttemplate='Rp %{y:,.0f}', textposition='outside', textfont_size=9)
fig7.update_layout(title=dict(text='Total Omset per Hari dalam Seminggu', x=0.01, font=dict(size=15)), yaxis=dict(zeroline=False))
save(fig7, '07_omset_per_hari', 420)

# ============================================================
# CHART 8: Dampak Hari Libur
# ============================================================
holiday_names = {'2026-01-01': 'Tahun Baru', '2026-01-29': "Isra Mi'raj",
                 '2026-02-17': 'Tahun Baru Imlek', '2026-03-19': 'Nyepi'}
hol_labels = ['Hari Normal']
hol_values = [df[~df['Tanggal'].dt.strftime('%Y-%m-%d').isin(holiday_names.keys())]['Omset'].mean()]
for date_str, name in holiday_names.items():
    d = pd.Timestamp(date_str)
    if d in df['Tanggal'].values:
        hol_labels.append(name)
        hol_values.append(df[df['Tanggal'] == d]['Omset'].sum())

fig8 = px.bar(x=hol_labels, y=hol_values, labels={'x': '', 'y': 'Omset (Rp)'})
fig8.update_traces(marker_color=[COLORS['primary']] + [COLORS['accent_coral']] * len(holiday_names),
                   texttemplate='Rp %{y:,.0f}', textposition='outside', textfont_size=10)
fig8.update_layout(title=dict(text='Dampak Hari Libur Nasional terhadap Omset', x=0.01, font=dict(size=15)), yaxis=dict(zeroline=False))
save(fig8, '08_dampak_libur', 420)

# ============================================================
# CHART 9: Proyeksi April + Garis Regresi
# ============================================================
monthly_omset = df.groupby('Bulan')['Omset'].sum()
last_date = df['Tanggal'].max()
forecast_dates = pd.date_range(start=last_date + timedelta(days=1), periods=30)
forecast_day_nums = np.array([(d - daily['Tanggal'].min()).days for d in forecast_dates])
forecast_values = trend_fn(forecast_day_nums)
apr_proj = forecast_values.sum()

month_start_days = {'Januari': 0, 'Februari': 31, 'Maret': 59, 'April': 90}
month_n_days = {'Januari': 31, 'Februari': 28, 'Maret': 31, 'April': 30}
months = ['Januari', 'Februari', 'Maret', 'April (Proyeksi)']
bar_heights = [monthly_omset['Januari'], monthly_omset['Februari'], monthly_omset['Maret'], apr_proj]
trend_straight = [trend_fn(month_start_days[m]) * month_n_days[m] for m in month_start_days]

fig9 = go.Figure()
fig9.add_trace(go.Bar(x=months, y=bar_heights, name='Omset',
                      marker_color=[COLORS['primary']] * 3 + [COLORS['accent_gold']],
                      text=[f'Rp {v:,.0f}' for v in bar_heights], textposition='outside', textfont_size=10))
fig9.add_trace(go.Scatter(x=months, y=trend_straight, name='Garis Regresi',
                          mode='lines', line=dict(color=COLORS['accent_rose'], width=3)))
fig9.update_layout(title=dict(text='Proyeksi 1 Bulan ke Depan + Garis Regresi', x=0.01, font=dict(size=15)),
                   xaxis_title='', yaxis_title='Omset (Rp)', yaxis=dict(rangemode='tozero'),
                   legend=dict(orientation='h', y=1.08, x=0.5, xanchor='center'))
save(fig9, '09_proyeksi_april', 450)

# ============================================================
# CHART 10: Tren Kategori per Bulan
# ============================================================
cat_monthly = df.groupby(['Bulan', 'Kategori'])['Omset'].sum().reset_index()
cat_monthly['Bulan'] = pd.Categorical(cat_monthly['Bulan'], categories=month_order, ordered=True)
cat_monthly = cat_monthly.sort_values('Bulan')

fig10 = px.bar(cat_monthly, x='Bulan', y='Omset', color='Kategori',
               color_discrete_sequence=CHART_COLORS[:len(cat_monthly['Kategori'].unique())],
               labels={'Omset': 'Total Omset (Rp)', 'Bulan': ''})
fig10.update_layout(title=dict(text='Omset Kategori per Bulan (Stacked)', x=0.01, font=dict(size=15)),
                    barmode='stack', legend=dict(orientation='h', y=1.15, x=0.5, xanchor='center'))
save(fig10, '10_kategori_stacked', 450)

# ============================================================
# CHART 11: Box Plot Distribusi per Cabang
# ============================================================
daily_branch = df.groupby(['Tanggal', 'Nama_Cabang'])['Omset'].sum().reset_index()
fig11 = px.box(daily_branch, x='Nama_Cabang', y='Omset',
               labels={'Omset': 'Omset (Rp)', 'Nama_Cabang': ''})
fig11.update_traces(marker_color=COLORS['primary'])
fig11.update_layout(title=dict(text='Distribusi Omset Harian per Cabang', x=0.01, font=dict(size=15)))
save(fig11, '11_boxplot_cabang', 450)

print(f'\nDone! {len(os.listdir(CHART_DIR))} charts saved to {CHART_DIR}/')
