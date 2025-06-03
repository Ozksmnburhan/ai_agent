import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import os

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="Gemini AI Ürün İçerik Üretici", layout="centered")

st.title("🛍️ AI Ürün Açıklama ve Başlık Oluşturucu (Gemini)")
st.caption("Görsel + açıklama ile SEO uyumlu içerikler üretin.")

uploaded_file = st.file_uploader("📸 Ürün fotoğrafını yükleyin (isteğe bağlı)", type=["jpg", "jpeg", "png"])
user_input = st.text_area("📝 Ürün hakkında kısa bilgi girin", placeholder="Örnek: El yapımı kahverengi deri çanta")

if st.button("✨ İçerik Üret"):
    if not user_input and not uploaded_file:
        st.warning("Lütfen en azından bir açıklama veya görsel girin.")
    else:
        with st.spinner("Gemini içerik oluşturuyor..."):
            parts = []

            if uploaded_file:
                uploaded_file.seek(0)  # Dosyanın başına git
                image_bytes = uploaded_file.read()
                parts.append({
                    "mime_type": uploaded_file.type,  # "image/jpeg" veya "image/png"
                    "data": image_bytes
                })


            if user_input:
                parts.append(f"""
                Aşağıdaki ürün bilgisine göre:
                1. Başlık (kısa ve dikkat çekici)
                2. Ürün açıklaması (profesyonel, SEO uyumlu)
                3. 5 adet hashtag
                
                Ürün açıklaması: {user_input}
                """)

            try:
                response = model.generate_content(parts)
                result = response.text.strip()
                st.success("🎉 İçerik oluşturuldu!")
                st.text_area("📋 Üretilen İçerik", value=result, height=300)
            except Exception as e:
                st.error(f"Hata oluştu: {e}")
