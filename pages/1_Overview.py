import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")

# قراءة التصميم
try:
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

chart_layout = dict(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#FAFAFA'), margin=dict(l=20, r=20, t=40, b=20))

@st.cache_data
def load_data():
    df = pd.read_csv('supermarket_advanced.csv')
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
    for col in ['net_sales', 'gross_profit', 'quantity', 'unit_price', 'profit_margin_percent', 'store_rating', 'customer_age']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

df = load_data()

# الفلاتر
st.sidebar.title("Filters")
date_min = df['transaction_date'].min()
date_max = df['transaction_date'].max()
if pd.notna(date_min) and pd.notna(date_max):
    date_range = st.sidebar.date_input("Date Range", value=(date_min.date(), date_max.date()), min_value=date_min.date(), max_value=date_max.date())

all_categories = sorted(df['product_category'].dropna().unique().tolist())
selected_categories = st.sidebar.multiselect("Product Category", options=all_categories, default=all_categories)

all_cities = sorted(df['store_city'].dropna().unique().tolist())
selected_cities = st.sidebar.multiselect("Store City", options=all_cities, default=all_cities)

filtered = df.copy()
if date_range and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[(filtered['transaction_date'].dt.date >= start_date) & (filtered['transaction_date'].dt.date <= end_date)]
if selected_categories:
    filtered = filtered[filtered['product_category'].isin(selected_categories)]
if selected_cities:
    filtered = filtered[filtered['store_city'].isin(selected_cities)]

st.session_state['filtered_data'] = filtered

# المحتوى
st.title("📊 Overview")
st.caption("نظرة عامة على أداء السوبر ماركت")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${filtered['net_sales'].sum():,.0f}")
col2.metric("Total Profit", f"${filtered['gross_profit'].sum():,.0f}")
col3.metric("Total Orders", f"{filtered['transaction_id'].nunique():,}")
col4.metric("Avg Basket Value", f"${filtered.groupby('transaction_id')['net_sales'].sum().mean():,.2f}")

st.markdown("---")

col_a, col_b = st.columns(2)
with col_a:
    st.subheader("Sales by Product Category")
    rev_cat = filtered.groupby('product_category')['net_sales'].sum().sort_values(ascending=True).reset_index()
    fig1 = px.bar(rev_cat, x='net_sales', y='product_category', orientation='h', color='net_sales', color_continuous_scale='Teal', text_auto='.2s')
    fig1.update_layout(showlegend=False, height=400, **chart_layout)
    fig1.update_coloraxes(showscale=False)
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.subheader("Sales Trend (Monthly)")
    trend = filtered.groupby('month_name')['net_sales'].sum().reset_index()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    trend['month_name'] = pd.Categorical(trend['month_name'], categories=month_order, ordered=True)
    trend = trend.sort_values('month_name')
    fig2 = px.line(trend, x='month_name', y='net_sales', markers=True, color_discrete_sequence=['#00E5FF'])
    fig2.update_layout(height=400, **chart_layout)
    st.plotly_chart(fig2, use_container_width=True)

# التقرير
st.markdown("---")
st.subheader("📥 تحميل التقرير")

report_data = pd.DataFrame({
    "المؤشر (KPI)": ["إجمالي المبيعات", "إجمالي الربح", "عدد الطلبات", "متوسط قيمة السلة"],
    "القيمة": [f"${filtered['net_sales'].sum():,.2f}", f"${filtered['gross_profit'].sum():,.2f}", f"{filtered['transaction_id'].nunique():,}", f"${filtered.groupby('transaction_id')['net_sales'].sum().mean():,.2f}"]
})
cat_sales = filtered.groupby('product_category')['net_sales'].sum().reset_index().sort_values("net_sales", ascending=False).head(10)
city_sales = filtered.groupby('store_city')['net_sales'].sum().reset_index().sort_values("net_sales", ascending=False)

buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    workbook = writer.book
    report_data.to_excel(writer, sheet_name='KPIs', index=False)
    cat_sales.to_excel(writer, sheet_name='Sales_by_Category', index=False)
    city_sales.to_excel(writer, sheet_name='Sales_by_City', index=False)
    
    # شارت الفئات
    chart_cat = workbook.add_chart({'type': 'bar'})
    chart_cat.add_series({'name': 'المبيعات', 'categories': ['Sales_by_Category', 1, 0, len(cat_sales), 0], 'values': ['Sales_by_Category', 1, 1, len(cat_sales), 1], 'fill': {'color': '#00E5FF'}})
    chart_cat.set_title({'name': 'أعلى 10 فئات'})
    chart_cat.set_legend({'none': True})
    chart_cat.set_size({'width': 600, 'height': 400})
    writer.sheets['Sales_by_Category'].insert_chart('D2', chart_cat)

    # شارت المدن
    chart_city = workbook.add_chart({'type': 'column'})
    chart_city.add_series({'name': 'المبيعات', 'categories': ['Sales_by_City', 1, 0, len(city_sales), 0], 'values': ['Sales_by_City', 1, 1, len(city_sales), 1], 'fill': {'color': '#8A2BE2'}})
    chart_city.set_title({'name': 'المبيعات حسب المدينة'})
    chart_city.set_legend({'none': True})
    chart_city.set_size({'width': 600, 'height': 400})
    writer.sheets['Sales_by_City'].insert_chart('D2', chart_city)

st.download_button(
    label="📊 تحميل التقرير (Excel)",
    data=buffer.getvalue(),
    file_name="supermarket_report.xlsx",
    mime="application/vnd.ms-excel",
    use_container_width=True
)