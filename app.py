import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import io
import requests

# إعداد واجهة التطبيق لتشبه تطبيق "ماكرون"
st.set_page_config(page_title="Arabic Thumbnail Maker", layout="wide")
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🎨 صانع الصور المصغرة الاحترافي</h1>", unsafe_allow_html=True)

# وظيفة لجلب الخط العربي من الإنترنت ليعمل على المتصفح مباشرة
@st.cache_data
def load_font():
    url = "https://github.com/google/fonts/raw/main/ofl/cairo/Cairo-Bold.ttf"
    return io.BytesIO(requests.get(url).content)

# القائمة الجانبية
with st.sidebar:
    st.header("🖼️ التحكم بالصورة")
    uploaded_file = st.file_uploader("ارفع الصورة التي ولدتها", type=["jpg", "png", "jpeg"])
    font_size = st.slider("حجم الخط العربي", 40, 250, 100)
    text_color = st.color_picker("لون العنوان", "#FFFFFF")
    stroke_color = st.color_picker("لون تحديد النص", "#000000")

# منطقة العمل الرئيسية
user_text = st.text_input("اكتب عنوان الفيديو هنا:", "أسرار الذكاء الاصطناعي")

if uploaded_file:
    # فتح الصورة ومعالجتها
    img = Image.open(uploaded_file).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    # إصلاح مشكلة الحروف العربية (من اليمين لليسار)
    reshaped_text = arabic_reshaper.reshape(user_text)
    bidi_text = get_display(reshaped_text)
    
    # تحميل الخط وتحديد مكانه (في المنتصف)
    font = ImageFont.truetype(load_font(), font_size)
    w, h = img.size
    
    # رسم النص مع "إطار" (Stroke) ليظهر بوضوح فوق أي خلفية
    draw.text((w/2, h/2), bidi_text, font=font, fill=text_color, 
              anchor="mm", stroke_width=3, stroke_fill=stroke_color)
    
    # عرض النتيجة
    st.image(img, use_container_width=True, caption="معاينة التصميم النهائي")
    
    # تحويل الصورة إلى ملف قابل للتحميل
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    st.download_button(label="📥 تحميل الصورة المصغرة الآن", 
                       data=img_byte_arr.getvalue(), 
                       file_name="my_thumbnail.png", 
                       mime="image/png")
else:
    st.warning("👈 من فضلك ارفع صورة من القائمة الجانبية للبدء.")
  
