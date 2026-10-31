# -*- coding: utf-8 -*-
import streamlit as st
import plotly.express as px
import pandas as pd

# إعدادات الشارتات (الثيم الأسود الفخم)
chart_layout = dict(
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)', 
    font=dict(color='#FAFAFA'), 
    margin=dict(l=20, r=20, t=40, b=20),
    staticPlot=True  # السطر السحري اللي بيثبت الشارت
)

st.title("📦 Inventory & Store Operations")
st.caption("تحليل المخزون وعمليات المتجر")

# بنجيب الداتا المفلترة من الملف الرئيسي
if 'filtered_data' in st.session_state:
    filtered = st.session_state['filtered_data']
else:
    st.warning("⚠️ رجاءً ارجع للصفحة الرئيسية أولاً لتطبيق الفلاتر.")
    st.stop()

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Low Stock Products (Top 10)")
    st.caption("أكتر 10 منتجات مخزونها بيقل (عشان تطلب توريد)")
    if 'low_stock_status' in filtered.columns:
        # بنفلتر المنتجات اللي حالتها Low Stock أو True
        low_stock = filtered[filtered['low_stock_status'].astype(str).str.lower().isin(['true', 'yes', '1'])]
        if not low_stock.empty:
            top_low = low_stock.groupby('product_name')['quantity'].sum().sort_values(ascending=False).head(10).reset_index()
            fig1 = px.bar(top_low, x='quantity', y='product_name', orientation='h', 
                          color='quantity', color_continuous_scale='Reds', text_auto='.2s')
            fig1.update_layout(showlegend=False, height=400, yaxis={'categoryorder': 'total ascending'}, **chart_layout)
            fig1.update_coloraxes(showscale=False)
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.success("✅ مفيش منتجات مخزونها قليل في الفترة دي!")

with col_b:
    st.subheader("Delivery Delays by Store City")
    st.caption("متوسط أيام تأخير التوصيل في كل مدينة")
    if 'delivery_delay_days' in filtered.columns:
        delays = filtered.groupby('store_city')['delivery_delay_days'].mean().sort_values(ascending=False).reset_index()
        fig2 = px.bar(delays, x='delivery_delay_days', y='store_city', orientation='h', 
                      color='delivery_delay_days', color_continuous_scale='Oranges', text_auto='.2f')
        fig2.update_layout(showlegend=False, height=400, yaxis={'categoryorder': 'total ascending'}, **chart_layout)
        fig2.update_coloraxes(showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# شارت تالت تحت: أعلى المنتجات في هامش الربح
st.subheader("Top 10 Products by Profit Margin")
st.caption("المنتجات اللي بتجيب أعلى نسبة ربح")
if 'profit_margin_percent' in filtered.columns:
    top_margin = filtered.groupby('product_name')['profit_margin_percent'].mean().sort_values(ascending=False).head(10).reset_index()
    fig3 = px.bar(top_margin, x='profit_margin_percent', y='product_name', orientation='h', 
                  color='profit_margin_percent', color_continuous_scale='Greens', text_auto='.1f')
    fig3.update_layout(showlegend=False, height=400, yaxis={'categoryorder': 'total ascending'}, **chart_layout)
    fig3.update_coloraxes(showscale=False)
    st.plotly_chart(fig3, use_container_width=True)