# -*- coding: utf-8 -*-
import streamlit as st
from groq import Groq

# ============================================================
# قراءة المفتاح من Secrets
# ============================================================
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except (KeyError, FileNotFoundError):
    GROQ_API_KEY = None

# ============================================================
# ضبط اتجاه الصفحة لليمين (RTL) وتكبير الخط
# ============================================================
st.markdown("""
<style>
    /* اتجاه الصفحة من اليمين لليسار */
    .stApp {
        direction: rtl;
        text-align: right;
    }
    
    /* تكبير الخطوط */
    p, li, .stMarkdown {
        font-size: 1.25rem !important;
        line-height: 1.8 !important;
    }
    
    /* تنسيق العناوين العربية */
    strong {
        font-size: 1.3rem !important;
        color: #00E5FF !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 AI Business Insights")
st.markdown("هنا الذكاء الاصطناعي هيقرأ الأرقام ويطلعلك توصيات احترافية.")

if 'filtered_data' in st.session_state:
    filtered = st.session_state['filtered_data']
else:
    st.warning("⚠️ رجاءً ارجع للصفحة الرئيسية أولاً لتطبيق الفلاتر.")
    st.stop()

if not GROQ_API_KEY:
    st.error("⚠️ مفيش API Key. تأكد إنك حطيت المفتاح في إعدادات Secrets على Streamlit Cloud.")
else:
    if st.button("✨ توليد التقرير بالـ AI", type="primary", use_container_width=True):
        try:
            kpis_text = f"""
            - إجمالي المبيعات: ${filtered['net_sales'].sum():,.2f}
            - إجمالي الربح: ${filtered['gross_profit'].sum():,.2f}
            - عدد الطلبات: {filtered['transaction_id'].nunique():,}
            - عدد العملاء: {filtered['customer_id'].nunique():,}
            - متوسط هامش الربح: {filtered['profit_margin_percent'].mean():.2f}%
            """
            
            top_cats = filtered.groupby('product_category')['net_sales'].sum().sort_values(ascending=False).head(5).reset_index()
            cats_text = "\n".join([f"- {row['product_category']}: ${row['net_sales']:,.2f}" for _, row in top_cats.iterrows()])

            # غيرنا العناوين لعربي عشان الترتيب ميلخبطش
            prompt = f"""
            أنت محلل بيانات أول في سوبر ماركت. عندك النتائج الإحصائية دي:
            
            KPIs:
            {kpis_text}
            
            أعلى 5 فئات في المبيعات:
            {cats_text}

            اكتب 5 توصيات احترافية، وكل توصية تكون بالشكل ده بالظبط (بدون استخدام كلمات إنجليزية في العناوين):
            - **ما هو:** الرقم أو الملاحظة (مع الرقم الدقيق)
            - **لماذا:** السبب المحتمل
            - **التأثير:** التأثير على البيزنس
            - **التوصية:** خطوة محددة وقابلة للتنفيذ

            القواعد: اكتب بالعربي المصري المبسط، وركز على الأرباح.
            """

            client = Groq(api_key=GROQ_API_KEY)
            st.info("⏳ جاري تحليل البيانات...")
            
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{"role": "user", "content": prompt}]
            )

            st.markdown("---")
            st.markdown(response.choices[0].message.content)
            st.success("✅ التقرير جاهز!")

        except Exception as e:
            st.error(f"حصل خطأ: {e}")