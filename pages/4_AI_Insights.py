# -*- coding: utf-8 -*-
from groq import Groq
import streamlit as st

st.markdown("""
<style>
    /* تكبير النصوص العادية والـ markdown */
    p, li, .stMarkdown {
        font-size: 1.25rem !important;
        line-height: 1.8 !important;
    }
    /* تكبير عناوين الـ Insights */
    strong {
        font-size: 1.3rem !important;
        color: #00E5FF !important; /* لون سماوي للعناوين */
    }
    /* تكبير عناوين الصفحة */
    h1 {
        font-size: 3.5rem !important;
    }
</style>
""", unsafe_allow_html=True)
# ============================================================
# ⚠️ حط مفتاح Groq بتاعك هنا (اللي بيبدأ بـ gsk_)
# ============================================================
GROQ_API_KEY = "ضع_المفتاح_هنا_او_في_سيكريتس"
# ============================================================

st.title("🤖 AI Business Insights")
st.markdown("هنا الذكاء الاصطناعي هيقرأ الأرقام ويطلعلك توصيات احترافية.")

if 'filtered_data' in st.session_state:
    filtered = st.session_state['filtered_data']
else:
    st.warning("⚠️ رجاءً ارجع للصفحة الرئيسية أولاً لتطبيق الفلاتر.")
    st.stop()

if not GROQ_API_KEY or GROQ_API_KEY == "حط_المفتاح_بتاعك_هنا":
    st.error("⚠️ مفيش API Key. تأكد إنك حطيت مفتاح Groq في الكود فوق.")
else:
    if st.button("✨ توليد التقرير بالـ AI", type="primary", use_container_width=True):
        try:
            # تجهيز الأرقام كـ نصوص عادية
            kpis_text = f"""
            - إجمالي المبيعات: ${filtered['net_sales'].sum():,.2f}
            - إجمالي الربح: ${filtered['gross_profit'].sum():,.2f}
            - عدد الطلبات: {filtered['transaction_id'].nunique():,}
            - عدد العملاء: {filtered['customer_id'].nunique():,}
            - متوسط هامش الربح: {filtered['profit_margin_percent'].mean():.2f}%
            """
            
            top_cats = filtered.groupby('product_category')['net_sales'].sum().sort_values(ascending=False).head(5).reset_index()
            cats_text = "\n".join([f"- {row['product_category']}: ${row['net_sales']:,.2f}" for _, row in top_cats.iterrows()])

            prompt = f"""
            أنت محلل بيانات أول في سوبر ماركت. عندك النتائج الإحصائية دي:
            
            KPIs:
            {kpis_text}
            
            أعلى 5 فئات في المبيعات:
            {cats_text}

            اكتب 5 insights احترافية بصيغة:
            - **What:** الرقم/الملاحظة
            - **Why:** السبب المحتمل
            - **So What:** التأثير على البيزنس
            - **Now What:** توصية محددة

            القواعد: اكتب بالعربي المصري المبسط، وركز على الأرباح.
            """

            # إعداد عميل Groq
            client = Groq(api_key=GROQ_API_KEY)
            
            st.info("⏳ جاري تحليل البيانات...")
            
            # طلب الرد من Groq (باستخدام موديل Llama)
            stream = client.chat.completions.create(
               model="openai/gpt-oss-120b", # موديل قوي ومجاني
                messages=[
                    {"role": "user", "content": prompt}
                ],
                stream=True
            )

            def stream_text():
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content

            st.markdown("---")
            st.write_stream(stream_text())
            st.success("✅ التقرير جاهز!")

        except Exception as e:
            st.error(f"حصل خطأ: {e}")