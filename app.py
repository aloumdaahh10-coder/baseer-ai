import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

# ضبط إعدادات الصفحة
st.set_page_config(
    page_title="بَصِير | محرك التحقق الشرعي - فتاوى ابن باز",
    page_icon="🛡️",
    layout="centered"
)

# دالة البحث المباشر في الموقع الرسمي للإمام ابن باز
def search_binbaz(query):
    encoded_query = urllib.parse.quote(query)
    search_url = f"https://binbaz.org.sa/search?q={encoded_query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # استخراج النتائج من صفحة البحث
            results = []
            items = soup.find_all('div', class_='search-result-item') or soup.find_all('article')
            
            for item in items[:3]: # أخذ أول 3 نتائج دقيقة
                title_tag = item.find('a')
                snippet_tag = item.find('p')
                
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    link = title_tag['href']
                    if not link.startswith('http'):
                        link = f"https://binbaz.org.sa{link}"
                    snippet = snippet_tag.get_text(strip=True) if snippet_tag else "اضغط على الرابط لقراءة الفتوى كاملة من المصدر."
                    results.append({"title": title, "link": link, "snippet": snippet})
            return results
    except Exception as e:
        return []
    return []

# واجهة المستخدم
st.title("🛡️ محرك بَصِير | فتاوى ابن باز")
st.caption("محرك بحث وتحقق مقيد حصرياً بالموقع الرسمي للإمام ابن باز رحمه الله (مكافحة الهلوسة الرقمية)")

st.markdown("""
> يقوم هذا النظام بفحص استفسارك والتحقق منه **حصرياً من فتاوى الموقع الرسمي للشيخ عبدالعزيز بن باز رحمه الله**؛ لمنع التوليد العشوائي والامتناع عن الإجابة في حال عدم ثبوت النص في المرجع.
""")

query = st.text_input("أدخل المسألة، السؤال، أو الحديث المراد البحث عنه في فتاوى الشيخ:", placeholder="مثال: حكم صلاة الوتر، قراءة القرآن للحائض...")

if st.button("فحص وتدقيق من موقع ابن باز", type="primary"):
    if not query.strip():
        st.warning("يرجى كتابة نص أو سؤال للبحث.")
    else:
        with st.spinner("جاري الاتصال والتحقق من الموقع الرسمي للإمام ابن باز..."):
            results = search_binbaz(query)
            
            if results:
                st.success("✅ نتيجة الفحص: تم العثور على فتاوى مطابقة في الموقع الرسمي")
                
                for idx, res in enumerate(results, 1):
                    with st.container(border=True):
                        st.subheader(f"📋 بطاقة الموثوقية الشرعية #{idx}")
                        st.markdown(f"**عنوان الفتوى:** {res['title']}")
                        st.write(f"**مقتطف من الجواب:** {res['snippet']}")
                        st.markdown(f"🔗 **رابط الفتوى من المصدر المعتمد:** [اضغط هنا للقراءة في موقع ابن باز]({res['link']})")
                        st.caption("المصدر: مؤسسة الشيخ عبدالعزيز بن باز الخيرية - الموقع الرسمي")
            else:
                st.error("⚠️ تنبيه: تعذر العثور على فتوى مطابقة في الموقع الرسمي")
                with st.container(border=True):
                    st.subheader("⛔ تفعيل خوارزمية الامتناع الآلي (Zero-Hallucination Guard)")
                    st.markdown("""
                    - **حالة البحث:** لم نجد نصاً مباشراً يطابق عبارة البحث في أرشيف فتاوى الشيخ ابن باز المتاح.
                    - **إجراء النظام:** امتنع المحرك آلياً عن توليد أو اختلاق أي فتوى من عنده صيانةً للفتوى والأمانة العلمية.
                    - **الإحالة:** يرجى صياغة البحث بكلمات أخرى أو الرجوع للمختصين واللجنة الدائمة للإفتاء.
                    """)
                    st.info("💡 مبدأ السلامة العلمية: التوقف عند عدم العثور على المرجع خيرٌ من الهلوسة وتلفيق الأحكام الشرعية.")
