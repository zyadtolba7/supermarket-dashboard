# -*- coding: utf-8 -*-
import streamlit as st
import plotly.express as px
import pandas as pd

chart_layout = dict(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#FAFAFA'), margin=dict(l=20, r=20, t=40, b=20))

st.title("👥 Customer Behavior & Loyalty")
st.caption("تحليل سلوك العملاء وولائهم")

if 'filtered_data' in st.session_state:
    filtered = st.session_state['filtered_data']
else:
    st.warning("⚠️ رجاءً ارجع للصفحة الرئيسية أولاً لتطبيق الفلاتر.")
    st.stop()

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Customer Segments")
    if 'customer_segment' in filtered.columns:
        seg_counts = filtered['customer_segment'].value_counts().reset_index()
        seg_counts.columns = ['Segment', 'Count']
        fig3 = px.pie(seg_counts, names='Segment', values='Count', hole=0.4, color_discrete_sequence=px.colors.sequential.Teal)
        fig3.update_layout(height=400, **chart_layout)
        fig3.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig3, use_container_width=True, config={'staticPlot': True})

with col_b:
    st.subheader("Churn Risk Distribution (مخاطر فقدان العملاء)")
    if 'customer_churn_risk' in filtered.columns:
        filtered['customer_churn_risk'] = pd.to_numeric(filtered['customer_churn_risk'], errors='coerce')
        bins = [-0.01, 0.25, 0.5, 0.75, 1.0]
        labels = ['Low Risk', 'Medium Risk', 'High Risk', 'Very High Risk']
        filtered['risk_category'] = pd.cut(filtered['customer_churn_risk'], bins=bins, labels=labels)
        churn = filtered['risk_category'].value_counts().reset_index()
        churn.columns = ['Risk Level', 'Count']
        fig4 = px.bar(churn, x='Risk Level', y='Count', color='Risk Level', color_discrete_sequence=px.colors.qualitative.Bold, text_auto=True)
        fig4.update_layout(showlegend=False, height=400, **chart_layout)
        st.plotly_chart(fig4, use_container_width=True, config={'staticPlot': True})

st.markdown("---")
st.subheader("Customer Age vs Loyalty Tier (الأعمار مقابل فئات الولاء)")

if 'customer_age' in filtered.columns and 'loyalty_tier' in filtered.columns:
    fig5 = px.box(filtered, x='loyalty_tier', y='customer_age', color='loyalty_tier', color_discrete_sequence=px.colors.sequential.Plasma)
    fig5.update_layout(showlegend=False, height=400, **chart_layout)
    st.plotly_chart(fig5, use_container_width=True, config={'staticPlot': True})