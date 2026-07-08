"""
Dashboard Interaktif - Analisis Penjualan PT Mensana Aneka Satwa
Jalankan: streamlit run dashboard.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(
    page_title="PT Mensana Aneka Satwa - Dashboard Penjualan",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# DESIGN SYSTEM - Colorful, Elegant, Presentation-Ready
# ============================================================
COLORS = {
    'primary': '#0F766E',
    'primary_light': '#14B8A6',
    'primary_dark': '#0D4F4F',
    'accent_gold': '#F59E0B',
    'accent_coral': '#F97316',
    'accent_blue': '#3B82F6',
    'accent_purple': '#8B5CF6',
    'accent_rose': '#F43F5E',
    'bg': '#F1F5F9',
    'card': '#FFFFFF',
    'text': '#1E293B',
    'text_muted': '#64748B',
    'text_light': '#94A3B8',
    'border': '#E2E8F0',
    'gradient_start': '#0F766E',
    'gradient_end': '#14B8A6',
}

CHART_COLORS = ['#14B8A6', '#F59E0B', '#3B82F6', '#F97316', '#8B5CF6',
                '#F43F5E', '#06B6D4', '#84CC16', '#EC4899', '#6366F1']

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* ---- GLOBAL ---- */
    .stApp {{
        background-color: {COLORS['bg']};
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}

    /* ---- HEADER ---- */
    .header-banner {{
        background: linear-gradient(135deg, {COLORS['primary_dark']} 0%, {COLORS['primary']} 40%, {COLORS['primary_light']} 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }}
    .header-banner::before {{
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: rgba(255,255,255,0.06);
        border-radius: 50%;
    }}
    .header-banner::after {{
        content: '';
        position: absolute;
        bottom: -60%;
        right: 5%;
        width: 200px;
        height: 200px;
        background: rgba(255,255,255,0.04);
        border-radius: 50%;
    }}
    .header-banner h1 {{
        color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 800;
        font-size: 1.8rem;
        margin: 0 !important;
        letter-spacing: -0.02em;
    }}
    .header-banner p {{
        color: rgba(255,255,255,0.85) !important;
        font-size: 0.95rem;
        margin: 0.3rem 0 0 0 !important;
    }}

    /* ---- KPI CARDS ---- */
    .kpi-card {{
        background: {COLORS['card']};
        border-radius: 14px;
        padding: 1.3rem 1.5rem;
        border: 1px solid {COLORS['border']};
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.03);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        position: relative;
        overflow: hidden;
    }}
    .kpi-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    }}
    .kpi-card .kpi-accent {{
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        border-radius: 14px 0 0 14px;
    }}
    .kpi-card .kpi-label {{
        color: {COLORS['text_muted']};
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.4rem;
    }}
    .kpi-card .kpi-value {{
        color: {COLORS['text']};
        font-size: 1.55rem;
        font-weight: 800;
        line-height: 1.2;
        letter-spacing: -0.02em;
    }}
    .kpi-card .kpi-sub {{
        color: {COLORS['text_light']};
        font-size: 0.78rem;
        margin-top: 0.3rem;
    }}

    /* ---- SECTION HEADERS ---- */
    .section-header {{
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin: 1.8rem 0 1rem 0;
    }}
    .section-header .section-icon {{
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        color: white;
    }}
    .section-header h3 {{
        color: {COLORS['text']} !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        margin: 0 !important;
    }}

    /* ---- CHART CARDS ---- */
    .chart-card {{
        background: {COLORS['card']};
        border-radius: 14px;
        padding: 1.2rem;
        border: 1px solid {COLORS['border']};
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        margin-bottom: 0.8rem;
    }}

    /* ---- TABLE ---- */
    .stDataFrame {{
        border-radius: 10px;
        overflow: hidden;
    }}

    /* ---- TABS ---- */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0;
        background: {COLORS['card']};
        border-radius: 12px;
        padding: 4px;
        border: 1px solid {COLORS['border']};
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.88rem;
        padding: 0.5rem 1.2rem;
        color: {COLORS['text_muted']};
    }}
    .stTabs [aria-selected="true"] {{
        background: {COLORS['primary']} !important;
        color: white !important;
    }}

    /* ---- SIDEBAR ---- */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COLORS['primary_dark']} 0%, {COLORS['primary']} 100%);
    }}
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {{
        color: rgba(255,255,255,0.9) !important;
    }}
    [data-testid="stSidebar"] label {{
        color: rgba(255,255,255,0.85) !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;
    }}
    [data-testid="stSidebarHeader"] {{
        color: white !important;
    }}

    /* ---- METRIC OVERRIDE ---- */
    [data-testid="stMetric"] {{
        background: transparent !important;
        padding: 0 !important;
    }}

    /* ---- FOOTER ---- */
    .footer {{
        background: linear-gradient(135deg, {COLORS['primary_dark']}, {COLORS['primary']});
        border-radius: 12px;
        padding: 1.2rem 2rem;
        margin-top: 2rem;
        text-align: center;
    }}
    .footer p {{
        color: rgba(255,255,255,0.8) !important;
        font-size: 0.82rem;
        margin: 0.2rem 0 !important;
    }}
    .footer strong {{
        color: white !important;
    }}

    /* ---- DIVIDER ---- */
    hr {{
        border: none;
        border-top: 1px solid {COLORS['border']};
        margin: 0.5rem 0;
    }}

    /* ---- STREAMLIT OVERRIDES ---- */
    [data-testid="stHorizontalBlock"] {{
        gap: 1rem;
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================
# CHART TEMPLATE
# ============================================================
CHART_TEMPLATE = dict(
    layout=go.Layout(
        font=dict(family='Plus Jakarta Sans, sans-serif', color=COLORS['text'], size=12),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(gridcolor=COLORS['border'], zeroline=False),
        yaxis=dict(gridcolor=COLORS['border'], zeroline=False),
        legend=dict(
            font=dict(size=11),
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor=COLORS['border'],
            borderwidth=1
        ),
        title=dict(font=dict(size=14, color=COLORS['text'], family='Plus Jakarta Sans'), x=0, xanchor='left'),
    )
)

def styled_fig(fig, height=400):
    fig.update_layout(**CHART_TEMPLATE['layout'])
    fig.update_layout(height=height)
    return fig

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    df = pd.read_excel('Data_Mentah_Harian.xlsx', sheet_name='Data_Penjualan_Harian')
    df_mapping = pd.read_excel('Data_Mentah_Harian.xlsx', sheet_name='Mapping_Produk')
    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    return df, df_mapping

df, df_mapping = load_data()

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style='padding: 0.5rem 0 1.2rem 0;'>
        <p style='color: rgba(255,255,255,0.5); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; margin: 0;'>Dashboard</p>
        <h2 style='color: white; margin: 0; font-weight: 800; font-size: 1.15rem;'>PT Mensana Aneka Satwa</h2>
        <p style='color: rgba(255,255,255,0.6); font-size: 0.78rem; margin: 0.3rem 0 0 0;'>Analisis Penjualan Q1 2026</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p style="color:rgba(255,255,255,0.5); font-size:0.72rem; text-transform:uppercase; letter-spacing:0.1em; margin-top:1rem;">FILTERS</p>', unsafe_allow_html=True)

    min_date = df['Tanggal'].min().date()
    max_date = df['Tanggal'].max().date()
    date_range = st.date_input(
        "Rentang Tanggal",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    branches = ['Semua Cabang'] + sorted(df['Nama_Cabang'].unique().tolist())
    selected_branch = st.selectbox("Cabang", branches)

    categories = ['Semua Kategori'] + sorted(df['Kategori'].unique().tolist())
    selected_category = st.selectbox("Kategori Produk", categories)

# Apply filters
if len(date_range) == 2:
    mask_date = (df['Tanggal'].dt.date >= date_range[0]) & (df['Tanggal'].dt.date <= date_range[1])
else:
    mask_date = df['Tanggal'].dt.date == date_range[0]

df_filtered = df[mask_date].copy()
if selected_branch != 'Semua Cabang':
    df_filtered = df_filtered[df_filtered['Nama_Cabang'] == selected_branch]
if selected_category != 'Semua Kategori':
    df_filtered = df_filtered[df_filtered['Kategori'] == selected_category]

# ============================================================
# HEADER
# ============================================================
st.markdown(f"""
<div class="header-banner">
    <h1>PT Mensana Aneka Satwa</h1>
    <p>Dashboard Analisis Penjualan - Periode Q1 2026 (Januari s/d Maret)</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# KPI CARDS
# ============================================================
total_omset = df_filtered['Omset'].sum()
total_qty = df_filtered['Kuantiti'].sum()
hari_aktif = df_filtered[df_filtered['Kuantiti'] > 0]['Tanggal'].nunique()
avg_daily = total_omset / max(hari_aktif, 1)
n_cabang = df_filtered['Nama_Cabang'].nunique()
n_produk = df_filtered['Nama_Standar'].nunique()

kpi_data = [
    ("Total Omset", f"Rp {total_omset:,.0f}", f"{n_cabang} cabang aktif", COLORS['primary']),
    ("Total Kuantiti", f"{total_qty:,.0f} unit", f"{n_produk} produk", COLORS['accent_gold']),
    ("Hari Aktif", f"{hari_aktif} hari", f"dari {df_filtered['Tanggal'].nunique()} hari", COLORS['accent_blue']),
    ("Rata-rata/Hari", f"Rp {avg_daily:,.0f}", "omset harian rata-rata", COLORS['accent_coral']),
]

kpi_html = '<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.5rem;">'
for label, value, sub, accent in kpi_data:
    kpi_html += f"""
    <div class="kpi-card">
        <div class="kpi-accent" style="background: {accent};"></div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>"""
kpi_html += '</div>'
st.markdown(kpi_html, unsafe_allow_html=True)

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3 = st.tabs(["Overview", "Cabang & Produk", "Analisis Lanjutan"])

# ============================================================
# TAB 1: OVERVIEW
# ============================================================
with tab1:
    col_left, col_right = st.columns(2)

    with col_left:
        cat_omset = df_filtered.groupby('Kategori')['Omset'].sum().sort_values(ascending=False)
        fig_cat = px.pie(
            values=cat_omset.values,
            names=cat_omset.index,
            hole=0.55,
            color_discrete_sequence=CHART_COLORS
        )
        fig_cat.update_traces(textposition='inside', textinfo='percent+label',
                              textfont_size=11, textfont_color='white',
                              hovertemplate='<b>%{label}</b><br>Rp %{value:,.0f}<br>%{percent}<extra></extra>')
        fig_cat.update_layout(
            title=dict(text='Distribusi Omset per Kategori', font=dict(size=14, color=COLORS['text'])),
            showlegend=False, height=380, margin=dict(t=50, b=10, l=10, r=10),
            annotations=[dict(text=f'<b>{len(cat_omset)}</b><br>Kategori', x=0.5, y=0.5,
                              font_size=14, showarrow=False, font_color=COLORS['text'])]
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_right:
        branch_omset = df_filtered.groupby('Nama_Cabang')['Omset'].sum().sort_values(ascending=True)
        branch_colors = [COLORS['primary'] if v > branch_omset.quantile(0.7)
                         else COLORS['accent_gold'] if v > branch_omset.quantile(0.3)
                         else COLORS['text_light'] for v in branch_omset.values]
        fig_branch = px.bar(
            x=branch_omset.values, y=branch_omset.index,
            orientation='h',
            labels={'x': 'Omset (Rp)', 'y': ''},
            color_discrete_sequence=[COLORS['primary']]
        )
        fig_branch.update_traces(
            marker_color=branch_colors,
            hovertemplate='<b>%{y}</b><br>Rp %{x:,.0f}<extra></extra>',
            text=[f'Rp {v/1e6:.1f}M' if v >= 1e9 else f'Rp {v/1e6:.0f}Jt' for v in branch_omset.values],
            textposition='outside', textfont_size=10, textfont_color=COLORS['text_muted']
        )
        fig_branch.update_layout(
            title=dict(text='Omset per Cabang', font=dict(size=14, color=COLORS['text'])),
            height=380, margin=dict(t=50, b=10, l=10, r=60),
            xaxis=dict(gridcolor=COLORS['border'], zeroline=False, showticklabels=False),
            yaxis=dict(gridcolor=COLORS['border'], tickfont=dict(size=11))
        )
        st.plotly_chart(fig_branch, use_container_width=True)

    # Daily trend with area fill
    daily_total = df_filtered.groupby('Tanggal')['Omset'].sum().reset_index()
    fig_daily = go.Figure()
    fig_daily.add_trace(go.Scatter(
        x=daily_total['Tanggal'], y=daily_total['Omset'],
        mode='lines', name='Omset Harian',
        line=dict(color=COLORS['primary'], width=2),
        fill='tozeroy',
        fillcolor='rgba(20,184,166,0.1)',
        hovertemplate='<b>%{x|%d %b %Y}</b><br>Rp %{y:,.0f}<extra></extra>'
    ))
    fig_daily.update_layout(
        title=dict(text='Tren Omset Harian', font=dict(size=14, color=COLORS['text'])),
        xaxis_title='', yaxis_title='Omset (Rp)',
        height=340, margin=dict(t=50, b=10),
        xaxis=dict(gridcolor=COLORS['border'], zeroline=False),
        yaxis=dict(gridcolor=COLORS['border'], zeroline=False)
    )
    st.plotly_chart(fig_daily, use_container_width=True)

# ============================================================
# TAB 2: CABANG & PRODUK
# ============================================================
with tab2:
    branch_stats = df_filtered.groupby(['ID_Cabang', 'Nama_Cabang', 'Provinsi']).agg(
        Total_Omset=('Omset', 'sum'),
        Total_Kuantiti=('Kuantiti', 'sum'),
        Rata_rata_Harian=('Omset', 'mean')
    ).reset_index().sort_values('Total_Omset', ascending=False)
    branch_stats['Persentase'] = (branch_stats['Total_Omset'] / branch_stats['Total_Omset'].sum() * 100).round(2)
    branch_stats['Ranking'] = range(1, len(branch_stats) + 1)

    st.markdown('<p style="font-weight:700; color:#1E293B; font-size:0.95rem;">Ranking Cabang</p>', unsafe_allow_html=True)
    st.dataframe(
        branch_stats[['Ranking', 'Nama_Cabang', 'Provinsi', 'Total_Omset', 'Persentase', 'Rata_rata_Harian']].style.format({
            'Total_Omset': 'Rp {:,.0f}',
            'Persentase': '{:.2f}%',
            'Rata_rata_Harian': 'Rp {:,.0f}'
        }),
        use_container_width=True, hide_index=True
    )

    # Progress per cabang per bulan
    month_order = ['Januari', 'Februari', 'Maret']
    progress = df_filtered.groupby(['Nama_Cabang', 'Bulan']).agg(Omset=('Omset', 'sum')).reset_index()
    progress['Bulan'] = pd.Categorical(progress['Bulan'], categories=month_order, ordered=True)
    progress = progress.sort_values(['Nama_Cabang', 'Bulan'])

    fig_progress = px.bar(
        progress, x='Nama_Cabang', y='Omset', color='Bulan',
        barmode='group', color_discrete_sequence=[COLORS['primary'], COLORS['accent_gold'], COLORS['accent_blue']],
        labels={'Omset': 'Omset (Rp)', 'Nama_Cabang': ''}
    )
    fig_progress.update_layout(
        title=dict(text='Progress Omset per Cabang per Bulan', font=dict(size=14, color=COLORS['text'])),
        height=420, margin=dict(t=50, b=10),
        xaxis=dict(gridcolor=COLORS['border'], tickangle=-35),
        yaxis=dict(gridcolor=COLORS['border']),
        legend=dict(orientation='h', y=1.08, x=0.5, xanchor='center')
    )
    st.plotly_chart(fig_progress, use_container_width=True)

    # Top 10 produk
    product_stats = df_filtered.groupby(['Nama_Standar', 'Kategori']).agg(
        Total_Omset=('Omset', 'sum')
    ).reset_index().sort_values('Total_Omset', ascending=False)

    cat_color_map = dict(zip(product_stats['Kategori'].unique(), CHART_COLORS))
    fig_top10 = px.bar(
        product_stats.head(10), x='Total_Omset', y='Nama_Standar',
        color='Kategori', orientation='h',
        color_discrete_map=cat_color_map,
        labels={'Total_Omset': 'Omset (Rp)', 'Nama_Standar': ''}
    )
    fig_top10.update_traces(
        texttemplate='Rp %{x:,.0f}', textposition='outside',
        textfont_size=10, textfont_color=COLORS['text_muted'],
        hovertemplate='<b>%{y}</b><br>Rp %{x:,.0f}<extra>%{fullData.name}</extra>'
    )
    fig_top10.update_layout(
        title=dict(text='Top 10 Produk Terlaris', font=dict(size=14, color=COLORS['text'])),
        height=400, margin=dict(t=50, b=10, r=80),
        xaxis=dict(gridcolor=COLORS['border'], zeroline=False),
        yaxis=dict(gridcolor=COLORS['border'], categoryorder='total ascending', tickfont=dict(size=11)),
        legend=dict(orientation='h', y=1.08, x=0.5, xanchor='center')
    )
    st.plotly_chart(fig_top10, use_container_width=True)

# ============================================================
# TAB 3: ANALISIS LANJUTAN
# ============================================================
with tab3:
    # Hari kerja vs weekend
    df_filtered_copy = df_filtered.copy()
    df_filtered_copy['Tipe_Hari'] = df_filtered_copy['Hari'].apply(
        lambda x: 'Akhir Pekan' if x in ['Sabtu', 'Minggu'] else 'Hari Kerja'
    )
    dow_comparison = df_filtered_copy.groupby('Tipe_Hari').agg(Rata_rata=('Omset', 'mean')).reset_index()

    col1, col2 = st.columns(2)

    with col1:
        fig_dow = px.bar(
            dow_comparison, x='Tipe_Hari', y='Rata_rata', color='Tipe_Hari',
            color_discrete_map={'Hari Kerja': COLORS['primary'], 'Akhir Pekan': COLORS['accent_coral']},
            labels={'Rata_rata': 'Rata-rata Omset (Rp)', 'Tipe_Hari': ''}
        )
        fig_dow.update_traces(
            texttemplate='Rp %{y:,.0f}', textposition='outside',
            textfont_size=10, textfont_color=COLORS['text_muted'],
            hovertemplate='<b>%{x}</b><br>Rp %{y:,.0f}<extra></extra>'
        )
        fig_dow.update_layout(
            title=dict(text='Hari Kerja vs Akhir Pekan', font=dict(size=14, color=COLORS['text'])),
            height=350, showlegend=False, margin=dict(t=50, b=10),
            xaxis=dict(gridcolor=COLORS['border']),
            yaxis=dict(gridcolor=COLORS['border'], zeroline=False)
        )
        st.plotly_chart(fig_dow, use_container_width=True)

    with col2:
        day_order = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
        dow_daily = df_filtered.groupby('Hari').agg(Total_Omset=('Omset', 'sum')).reindex(day_order).reset_index()
        dow_colors = [COLORS['primary']] * 5 + [COLORS['accent_coral']] * 2

        fig_dow2 = px.bar(
            dow_daily, x='Hari', y='Total_Omset',
            color_discrete_sequence=dow_colors,
            labels={'Total_Omset': 'Omset (Rp)', 'Hari': ''}
        )
        fig_dow2.update_traces(
            marker_color=dow_colors,
            texttemplate='Rp %{y:,.0f}', textposition='outside',
            textfont_size=9, textfont_color=COLORS['text_muted'],
            hovertemplate='<b>%{x}</b><br>Rp %{y:,.0f}<extra></extra>'
        )
        fig_dow2.update_layout(
            title=dict(text='Omset per Hari dalam Seminggu', font=dict(size=14, color=COLORS['text'])),
            height=350, showlegend=False, margin=dict(t=50, b=10),
            xaxis=dict(gridcolor=COLORS['border']),
            yaxis=dict(gridcolor=COLORS['border'], zeroline=False)
        )
        st.plotly_chart(fig_dow2, use_container_width=True)

    # Holiday impact
    holidays = {
        '2026-01-01': 'Tahun Baru', '2026-01-29': "Isra Mi'raj",
        '2026-02-17': 'Tahun Baru Imlek', '2026-03-19': 'Nyepi'
    }
    holiday_data = []
    for date_str, name in holidays.items():
        date = pd.Timestamp(date_str)
        if date in df_filtered['Tanggal'].values:
            holiday_omset = df_filtered[df_filtered['Tanggal'] == date]['Omset'].sum()
            surrounding = df_filtered[
                (df_filtered['Tanggal'] >= date - timedelta(days=3)) &
                (df_filtered['Tanggal'] <= date + timedelta(days=3)) &
                (df_filtered['Tanggal'] != date) &
                (~df_filtered['Tanggal'].dt.dayofweek.isin([5, 6]))
            ]
            avg_normal = surrounding.groupby('Tanggal')['Omset'].sum().mean()
            penurunan = ((avg_normal - holiday_omset) / avg_normal * 100) if avg_normal > 0 else 0
            holiday_data.append({
                'Tanggal': date_str, 'Libur': name,
                'Omset Libur': holiday_omset, 'Omset Normal': avg_normal, 'Penurunan (%)': penurunan
            })

    if holiday_data:
        df_holiday = pd.DataFrame(holiday_data)
        st.dataframe(
            df_holiday.style.format({'Omset Libur': 'Rp {:,.0f}', 'Omset Normal': 'Rp {:,.0f}', 'Penurunan (%)': '{:.1f}%'}),
            use_container_width=True, hide_index=True
        )

    # Alert
    daily_omset = df_filtered.groupby('Tanggal')['Omset'].sum().reset_index()
    mean_omset = daily_omset['Omset'].mean()
    std_omset = daily_omset['Omset'].std()
    threshold_low = mean_omset - 2 * std_omset
    threshold_high = mean_omset + 2 * std_omset
    daily_omset['Status'] = daily_omset['Omset'].apply(
        lambda x: 'Abnormal Rendah' if x < threshold_low else ('Abnormal Tinggi' if x > threshold_high else 'Normal')
    )
    abnormal = daily_omset[daily_omset['Status'] != 'Normal']

    if len(abnormal) > 0:
        abnormal['Tanggal_Str'] = abnormal['Tanggal'].dt.strftime('%Y-%m-%d')
        abnormal['Libur'] = abnormal['Tanggal_Str'].map(holidays).fillna('-')
        st.dataframe(
            abnormal[['Tanggal', 'Omset', 'Status', 'Libur']].style.format({'Omset': 'Rp {:,.0f}'}),
            use_container_width=True, hide_index=True
        )

        fig_alert = go.Figure()
        fig_alert.add_trace(go.Scatter(
            x=daily_omset['Tanggal'], y=daily_omset['Omset'],
            mode='lines+markers', name='Omset Harian',
            line=dict(color=COLORS['primary'], width=1.5),
            marker=dict(size=4, color=COLORS['primary']),
            hovertemplate='%{x|%d %b}<br>Rp %{y:,.0f}<extra></extra>'
        ))
        fig_alert.add_hline(y=threshold_high, line_dash="dash", line_color=COLORS['accent_coral'], line_width=1.5,
                           annotation_text="Threshold Atas", annotation_font_color=COLORS['accent_coral'])
        fig_alert.add_hline(y=threshold_low, line_dash="dash", line_color=COLORS['accent_rose'], line_width=1.5,
                           annotation_text="Threshold Bawah", annotation_font_color=COLORS['accent_rose'])
        fig_alert.add_hline(y=mean_omset, line_dash="solid", line_color=COLORS['accent_blue'], line_width=1.5,
                           annotation_text="Rata-rata", annotation_font_color=COLORS['accent_blue'])
        fig_alert.update_layout(
            title=dict(text='Monitoring Penjualan Harian', font=dict(size=14, color=COLORS['text'])),
            xaxis_title='', yaxis_title='Omset (Rp)',
            height=380, margin=dict(t=50, b=10),
            xaxis=dict(gridcolor=COLORS['border']),
            yaxis=dict(gridcolor=COLORS['border'])
        )
        st.plotly_chart(fig_alert, use_container_width=True)

    # Proyeksi
    daily_omset_proj = df_filtered.groupby('Tanggal')['Omset'].sum().reset_index()
    daily_omset_proj['day_num'] = (daily_omset_proj['Tanggal'] - daily_omset_proj['Tanggal'].min()).dt.days
    coeffs = np.polyfit(daily_omset_proj['day_num'], daily_omset_proj['Omset'], 1)
    trend_fn = np.poly1d(coeffs)
    last_date = daily_omset_proj['Tanggal'].max()
    forecast_dates = pd.date_range(start=last_date + timedelta(days=1), periods=30)
    forecast_day_nums = np.array([(d - daily_omset_proj['Tanggal'].min()).days for d in forecast_dates])
    forecast_values = trend_fn(forecast_day_nums)
    monthly_omset = df_filtered.groupby('Bulan')['Omset'].sum()
    apr_proj = forecast_values.sum()

    base_date = daily_omset_proj['Tanggal'].min()
    month_start_days = {
        'Januari': 0, 'Februari': 31, 'Maret': 59, 'April': 90,
    }
    month_n_days = {'Januari': 31, 'Februari': 28, 'Maret': 31, 'April': 30}
    bar_heights = [monthly_omset.get('Januari', 0), monthly_omset.get('Februari', 0), monthly_omset.get('Maret', 0), apr_proj]
    trend_straight = [trend_fn(month_start_days[m]) * month_n_days[m] for m in ['Januari', 'Februari', 'Maret', 'April']]

    # KPI inline
    proj_kpi_html = f"""
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.8rem; margin-bottom: 1rem;">
        <div class="kpi-card">
            <div class="kpi-accent" style="background: {COLORS['primary']};"></div>
            <div class="kpi-label">Maret 2026 (Aktual)</div>
            <div class="kpi-value" style="font-size:1.15rem;">Rp {monthly_omset.get('Maret', 0):,.0f}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-accent" style="background: {COLORS['accent_coral']};"></div>
            <div class="kpi-label">April 2026 (Proyeksi)</div>
            <div class="kpi-value" style="font-size:1.15rem;">Rp {apr_proj:,.0f}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-accent" style="background: {COLORS['accent_gold']};"></div>
            <div class="kpi-label">Trend Slope</div>
            <div class="kpi-value" style="font-size:1.15rem;">+Rp {coeffs[0]:,.0f}/hari</div>
        </div>
    </div>
    """
    st.markdown(proj_kpi_html, unsafe_allow_html=True)

    months = ['Januari', 'Februari', 'Maret', 'April\n(Proyeksi)']
    bar_colors = [COLORS['primary'], COLORS['primary'], COLORS['primary'], COLORS['accent_gold']]

    fig_proj = go.Figure()
    fig_proj.add_trace(go.Bar(
        x=months, y=bar_heights, name='Omset',
        marker_color=bar_colors,
        marker_line=dict(width=0),
        text=[f'Rp {v:,.0f}' for v in bar_heights],
        textposition='outside', textfont=dict(size=10, color=COLORS['text_muted']),
        hovertemplate='<b>%{x}</b><br>Rp %{y:,.0f}<extra></extra>'
    ))
    fig_proj.add_trace(go.Scatter(
        x=months, y=trend_straight, name='Garis Regresi',
        mode='lines', line=dict(color=COLORS['accent_rose'], width=3)
    ))
    fig_proj.update_layout(
        title=dict(text='Proyeksi 1 Bulan ke Depan + Garis Regresi', font=dict(size=14, color=COLORS['text'])),
        xaxis_title='', yaxis_title='Omset (Rp)',
        height=420, margin=dict(t=50, b=10),
        xaxis=dict(gridcolor=COLORS['border']),
        yaxis=dict(gridcolor=COLORS['border'], rangemode='tozero'),
        legend=dict(orientation='h', y=1.08, x=0.5, xanchor='center')
    )
    st.plotly_chart(fig_proj, use_container_width=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown(f"""
<div class="footer">
    <p><strong>PT Mensana Aneka Satwa</strong> | Dashboard Analisis Penjualan</p>
    <p>Periode: Januari - Maret 2026 (Q1) | 10 Cabang Distributor | 15 Produk Unggulan</p>
</div>
""", unsafe_allow_html=True)
