import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import io, requests

# إعداد التطبيق
st.set_page_config(page_title="AI Thumbnail Pro", layout="wide")
st.title("🎨 مولد الصور المصغرة مع اختيار المقاسات")

@st.cache_data
def load_font():
    return io.BytesIO(requests.get("https://github.com/googlefonts/cairo/raw/master/fonts/ttf/Cairo-Bold.ttf").content)

# القائمة الجانبية للمقاسات والإعدادات
with st.sidebar:
    st.header("📏 إعدادات الصورة")
    # إضافة خاصية المقاسات
    ratio = st.selectbox("اختر مقاس الصورة:", 
                         ["16:9 (يوتيوب)", "9:16 (تيك توك/ستوري)", "1:1 (إنستغرام)"])
    
    # تحديد العرض والطول بناءً على الاختيار
    if ratio == "16:9 (يوتيوب)":
        width, height = 1280, 720
    elif ratio == "9:16 (تيك توك/ستوري)":
        width, height = 720, 1280
    else:
        width, height = 1024, 1024

    font_size = st.slider("حجم الخط", 40, 300, 100)
    text_color = st.color_picker("لون الخط", "#FFFFFF")

# المدخلات الأساسية في الصفحة
prompt = st.text_input("صف الصورة بالإنجليزي:", "A high-tech workspace with neon lights")
title = st.text_input("العنوان العربي:", "تطوير التطبيقات")

if st.button("توليد وتصميم بالذكاء الاصطناعي 🚀"):
    with st.spinner("جاري التوليد بالمقاس المطلوب..."):
        # توليد الصورة مع تمرير العرض والطول للمحرك
        url = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width={width}&height={height}&seed=99"
        
        try:
            res = requests.get(url)
            img = Image.open(io.BytesIO(res.content)).convert("RGB")
            draw = ImageDraw.Draw(img)
            
            # معالجة النص العربي
            font = ImageFont.truetype(load_font(), font_size)
            text = get_display(arabic_reshaper.reshape(title))
            
            # وضع النص في منتصف الصورة بناءً على المقاس المختار
            draw.text((width/2, height/2), text, font=font, fill=text_color, 
                      anchor="mm", stroke_width=4, stroke_fill="black")
            
            st.image(img, use_container_width=True, caption=f"مقاس الصورة: {ratio}")
            
            # زر التحميل
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.download_button(f"📥 تحميل صورة ({ratio})", buf.getvalue(), "ai_thumbnail.png")
            
        except Exception as e:
            st.error("حدث خطأ، تأكد من الاتصال بالإنترنت.")
