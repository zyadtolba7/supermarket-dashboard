# -*- coding: utf-8 -*-
import sys
import streamlit as st

# ============================================================
# إجبار السيرفر على استخدام UTF-8 (بطريقة آمنة)
# ============================================================
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
# ============================================================

st.set_page_config(page_title="Supermarket Analytics", page_icon="🛒", layout="wide")

# قراءة التصميم
try:
    with open("style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# تصميم شاشة الترحيب
st.markdown("""
<style>
    .hero-title {
        font-size: 5rem !important;
        font-weight: 900 !important;
        color: #00E5FF !important;
        text-align: center;
        margin-bottom: 0px;
    }
    .hero-subtitle {
        font-size: 2rem !important;
        color: #FAFAFA !important;
        text-align: center;
        margin-bottom: 50px;
    }
    .stButton>button {
        display: block;
        margin: 0 auto;
        font-size: 2rem !important;
        padding: 15px 40px !important;
        background-color: #00E5FF !important;
        color: #0E1117 !important;
        border-radius: 15px !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div style='text-align: center; font-size: 8rem; margin-top: 50px;'>🛒</div>", unsafe_allow_html=True)
st.markdown('<div class="hero-title">Supermarket Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">منصة تحليل البيانات المتقدمة والذكاء الاصطناعي</div>', unsafe_allow_html=True)

if st.button("🚀 ابدأ التحليل"):
    st.switch_page("pages/1_Overview.py")