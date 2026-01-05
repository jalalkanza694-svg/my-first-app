import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import io, requests

st.set_page_config(page_title="AI Thumbnail Pro", layout="wide")
st.title("🎨 مولد الصور المصغرة الذكي")

def get_image_font(font_size):
    try:
        # محاولة تحميل خط القاهرة
        url = "https://github.com/googlefonts/cairo/raw/master/fonts/ttf/Cairo-Bold.ttf"
        response = requests.get(url, timeout=5)
        return ImageFont.truetype(io.BytesIO(response.content), font_size)
    except:
        # في حال الفشل، استخدم الخط الافتراضي للنظام لضمان عدم توقف التطبيق
        return ImageFont.load_default()

with st.sidebar:
    st.header("📏 الإعدادات")
    ratio = st.selectbox("اختر المقاس:", ["16:9 (يوتيوب)", "9:16 (تيك توك)", "1:1"])
    width, height = (1280, 720) if "16:9" in ratio else ((720, 1280) if "9:16" in ratio else (1024, 1024))
    font_size = st.slider("حجم الخط", 50, 250, 100)

prompt = st.text_input("صف الصورة بالإنجليزي:", "A high quality cinematic lion")
title = st.text_input("العنوان العربي:", "ملك المستقبل")

if st.button("توليد وتصميم 🚀"):
    with st.spinner("جاري التوليد..."):
        # محرك توليد الصور
        url = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width={width}&height={height}&seed=1"
        try:
            res = requests.get(url, timeout=15)
            img = Image.open(io.BytesIO(res.content)).convert("RGB")
            draw = ImageDraw.Draw(img)
            
            # معالجة النص
            font = get_image_font(font_size)
            reshaped_text = arabic_reshaper.reshape(title)
            bidi_text = get_display(reshaped_text)
            
            # الرسم
            draw.text((width/2, height/2), bidi_text, font=font, fill="white", anchor="mm", stroke_width=4, stroke_fill="black")
            
            st.image(img, use_container_width=True)
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.download_button("📥 تحميل الصورة", buf.getvalue(), "image.png")
        except:
            st.error("السيرفر مشغول، حاول مرة أخرى بعد لحظات.")
    
