import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import io, requests, time

st.set_page_config(page_title="AI Thumbnail Pro", layout="wide")
st.title("🎨 مولد الصور الاحترافي (نسخة الطوارئ)")

@st.cache_data
def load_font():
    return io.BytesIO(requests.get("https://github.com/googlefonts/cairo/raw/master/fonts/ttf/Cairo-Bold.ttf").content)

with st.sidebar:
    st.header("📏 الإعدادات")
    ratio = st.selectbox("اختر المقاس:", ["16:9 (يوتيوب)", "9:16 (تيك توك)", "1:1"])
    width, height = (1280, 720) if "16:9" in ratio else ((720, 1280) if "9:16" in ratio else (1024, 1024))
    font_size = st.slider("حجم الخط", 50, 250, 100)

prompt = st.text_input("صف الصورة بالإنجليزي:", "A high quality cinematic shot of a futuristic lion")
title = st.text_input("العنوان العربي:", "ملك المستقبل")

if st.button("توليد وتصميم 🚀"):
    with st.spinner("جاري محاولة التوليد من السيرفر..."):
        # المحرك الأول
        url1 = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width={width}&height={height}&seed={time.time()}"
        # المحرك الثاني (احتياطي)
        url2 = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width={width}&height={height}&nologo=true"
        
        img = None
        for target_url in [url1, url2]:
            try:
                res = requests.get(target_url, timeout=20)
                if res.status_code == 200:
                    img = Image.open(io.BytesIO(res.content)).convert("RGB")
                    break
            except:
                continue
        
        if img:
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype(load_font(), font_size)
            text = get_display(arabic_reshaper.reshape(title))
            draw.text((width/2, height/2), text, font=font, fill="white", anchor="mm", stroke_width=4, stroke_fill="black")
            st.image(img, use_container_width=True)
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.download_button("📥 تحميل الصورة", buf.getvalue(), "thumb.png")
        else:
            st.error("السيرفر العالمي مشغول حالياً، يرجى المحاولة مرة أخرى بعد دقيقة واحدة.")
