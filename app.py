import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import io, requests, random

st.set_page_config(page_title="AI Thumbnail Pro", layout="wide")
st.title("🎨 مولد الصور المصغرة الذكي")

# حل مشكلة الخط: محاولة تحميل الخط، وإذا فشل يستخدم خط النظام الافتراضي
def get_safe_font(size):
    try:
        url = "https://github.com/googlefonts/cairo/raw/master/fonts/ttf/Cairo-Bold.ttf"
        return ImageFont.truetype(io.BytesIO(requests.get(url, timeout=5).content), size)
    except:
        return ImageFont.load_default()

with st.sidebar:
    st.header("📏 الإعدادات")
    ratio = st.selectbox("اختر المقاس:", ["16:9 (يوتيوب)", "9:16 (تيك توك)", "1:1"])
    width, height = (1280, 720) if "16:9" in ratio else ((720, 1280) if "9:16" in ratio else (1024, 1024))
    font_size = st.slider("حجم الخط", 50, 200, 100)

prompt = st.text_input("صف الصورة بالإنجليزي:", "A high quality cinematic lion")
title = st.text_input("العنوان العربي:", "ملك المستقبل")

if st.button("توليد وتصميم 🚀"):
    if not prompt or not title:
        st.warning("الرجاء إدخال الوصف والعنوان!")
    else:
        with st.spinner("جاري التوليد..."):
            # حل مشكلة السيرفر: استخدام روابط مختلفة عند كل محاولة
            seed = random.randint(1, 1000)
            url = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width={width}&height={height}&seed={seed}"
            
            try:
                res = requests.get(url, timeout=20)
                if res.status_code == 200:
                    img = Image.open(io.BytesIO(res.content)).convert("RGB")
                    draw = ImageDraw.Draw(img)
                    
                    # رسم النص العربي
                    font = get_safe_font(font_size)
                    text = get_display(arabic_reshaper.reshape(title))
                    draw.text((width/2, height/2), text, font=font, fill="white", anchor="mm", stroke_width=4, stroke_fill="black")
                    
                    st.image(img, use_container_width=True)
                    buf = io.BytesIO()
                    img.save(buf, format="PNG")
                    st.download_button("📥 تحميل الصورة", buf.getvalue(), "image.png")
                else:
                    st.error("السيرفر العالمي مضغوط حالياً، يرجى إعادة المحاولة بعد ثوانٍ.")
            except:
                st.error("حدث خطأ في الاتصال، جرب مرة أخرى.")
    
    
