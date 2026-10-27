import streamlit as st
from google import genai

# إعدادات صفحة Streamlit
st.set_page_config(
    page_title="نقّاد - Naqqad",
    page_icon="🎯",
    layout="centered"
)

# تخصيص التصميم الداكن للواجهة
st.markdown("""
    <style>
    .stApp {
        background-color: #121620;
        color: #ffffff;
    }
    .main-title {
        text-align: center;
        font-size: 2.3rem;
        font-weight: bold;
        color: #ffffff;
    }
    .sub-title {
        text-align: center;
        font-size: 1.05rem;
        color: #94a3b8;
        margin-bottom: 25px;
    }
    .stTextArea textarea {
        background-color: #1e2535 !important;
        color: #ffffff !important;
        border: 1px solid #2d3748 !important;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# ترويسة التطبيق والشعار
st.markdown('<p class="main-title">🎯 نقّاد - Naqqad</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">المنصة الذكية الشاملة لكشف الشائعات والأخبار المضللة ورسائل الاحتيال</p>', unsafe_allow_html=True)

# تهيئة العميل باستخدام المفتاح
 #  نقرأه بأمان من أسرار المنصة
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=GEMINI_API_KEY)

# القائمة الجانبية للاختيار بين الأقسام
st.sidebar.markdown("### 🧭 أقسام منصة نقّاد")
app_mode = st.sidebar.selectbox(
    "اختر خدمة الفحص:",
    ["📰 فحص الشائعات والأخبار", "🚨 كشف الرسائل الاحتيالية"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 منصة نقّاد تستخدم تقنيات الذكاء الاصطناعي المتقدمة لتحليل النصوص ومحاربة المحتوى المضلل.")

# --- القسم الأول: فحص الشائعات والأخبار المضللة ---
if app_mode == "📰 فحص الشائعات والأخبار":
    st.markdown("### 📰 فحص وتحليل الشائعات والأخبار")
    st.markdown("ضع الخبر أو النص المراد التحقق من مصداقيته أدناه:")
    
    rumor_input = st.text_area("نص الخبر المشكوك فيه:", placeholder="...أدخل نص الخبر أو الإعلان هنا", key="rumor_box")
    
    if st.button("فحص الخبر والتحقق منه 🔍"):
        if rumor_input.strip():
            with st.spinner("جاري الفحص السريع..."):
                try:
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=f"أنت محلل في منصة 'نقّاد'. حلل النص باختصار شديد ومباشر (التصنيف: صحيح أو شائعة، ثم أسباب موجزة جداً):\n\n{rumor_input}"
                    )
                    st.success("تم التحليل بنجاح!")
                    st.markdown("### 📊 نتيجة التحليل:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"حدث خطأ مؤقت: يرجى المحاولة مرة أخرى.")
        else:
            st.warning("الرجاء إدخال نص الخبر أولاً.")

# --- القسم الثاني: كشف الرسائل الاحتيالية ---
elif app_mode == "🚨 كشف الرسائل الاحتيالية":
    st.markdown("### 🚨 كشف الرسائل الاحتيالية والروابط المشبوهة")
    st.markdown("ضع نص الرسالة النصية أو البريد الإلكتروني الاحتيالي المفترض أدناه:")
    
    fraud_input = st.text_area("نص الرسالة المشبوهة:", placeholder="...أدخل نص الرسالة أو العرض الوهمي هنا", key="fraud_box")
    
    if st.button("فحص الرسالة الاحتيالية 🛡️"):
        if fraud_input.strip():
            with st.spinner("جاري الفحص السريع..."):
                try:
                    # تم تبسيط تمرير النص لضمان عدم حدوث أي خطأ في الترميز
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=f"أنت خبير أمن في منصة 'نقّاد'. حلل الرسالة التالية باختصار شديد ومباشر (التصنيف: آمنة أو احتيالية، مع الأسباب باختصار):\n\n{fraud_input}"
                    )
                    st.success("تم الفحص بنجاح!")
                    st.markdown("### 📊 نتيجة تحليل الاحتيال:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"حدث خطأ مؤقت: يرجى المحاولة مرة أخرى.")
        else:
            st.warning("الرجاء إدخال نص الرسالة أولاً.")
