import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# --- إعدادات الصفحة ---
st.set_page_config(page_title="نقّاد - Naqqad", page_icon="🎯", layout="centered")

# --- تصميم الخلفية والتنسيقات (CSS) ---
st.markdown("""
    <style>
    /* خلفية متدرجة وأنيقة للموقع */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        color: #f8fafc;
    }
    
    /* تنسيق العنوان الرئيسي */
    .main-title {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 800;
        color: #38bdf8;
        margin-bottom: 0.2rem;
    }
    
    .sub-title {
        text-align: center;
        font-size: 1.2rem;
        color: #94a3b8;
        margin-bottom: 2rem;
    }

    /* تحسين شكل مربع النص */
    .stTextArea textarea {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        font-size: 1.05rem !important;
    }
    .stTextArea textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.3) !important;
    }

    /* تحسين زر الفحص */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #0284c7 0%, #2563eb 100%);
        color: white;
        font-size: 1.1rem;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #0369a1 0%, #1d4ed8 100%);
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# --- بيانات التدريب النموذجية ---
data = {
    'text': [
        "مبروك لقد ربحت معنا سيارة سجل بياناتك الآن لاستلام الجائزة",
        "عزيزي العميل تم تجميد حسابك البنكي الرجاء تحديث البيانات فوراً عبر الرابط",
        "احصل على تمويل شخصي بدون كفيل وبإجراءات سريعة تواصل معنا",
        "تم إرسال طلبك رقم 4092 مع مندوب التوصيل وسيتواصل معك قريباً",
        "عزيزي الطالب نود إحاطتك علماً بأن موعد الاختبارات النهائية سيبدأ الأحد القادم",
        "تذكير لديك موعد في العيادة غداً الساعة 10 صباحاً"
    ],
    'label': ['phishing', 'phishing', 'phishing', 'legitimate', 'legitimate', 'legitimate']
}

df = pd.DataFrame(data)

# --- تدريب النموذج ---
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['text'])
y = df['label']

model = MultinomialNB()
model.fit(X, y)

# --- واجهة المستخدم ---
st.markdown('<h1 class="main-title">🎯 نقّاد - Naqqad</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">نظام ذكي لكشف الرسائل الاحتيالية بأساليبها المحلية</p>', unsafe_allow_html=True)

user_input = st.text_area("ضع نص الرسالة أو البريد الإلكتروني المشكوك فيه أدناه لفحصه:", height=120, placeholder="أدخل نص الرسالة هنا...")

if st.button("🔍 فحص الرسالة الآن"):
    if user_input.strip() == "":
        st.warning("يرجى إدخال نص الرسالة أولاً!")
    else:
        text_vec = vectorizer.transform([user_input])
        prediction = model.predict(text_vec)[0]
        proba = model.predict_proba(text_vec)[0]
        confidence = max(proba) * 100
        
        st.markdown("---")
        if prediction == 'phishing':
            st.error(f"🚨 **تنبيه: الرسالة قد تكون احتيالية!** (نسبة الثقة: {confidence:.1f}%)")
        else:
            st.success(f"✅ **الرسالة آمنة** (نسبة الثقة: {confidence:.1f}%)")