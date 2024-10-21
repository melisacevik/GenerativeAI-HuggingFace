import streamlit as st
import cv2
import numpy as np
from dotenv import load_dotenv
import os
import google.generativeai as genai
import time
import logging

# .env dosyasını yükle
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Google Generative AI ayarları
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
]


model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings=safety_settings,
)

st.title("Kahve Fincanı Yorumlama")

user_photo = st.file_uploader("Bir kahve fincanı fotoğrafı yükleyiniz")

def generate_response(prompt):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            logging.error(f"Full error: {str(e)}")
            st.error(f"Error: {str(e)}")
            time.sleep(2)
    st.error("Failed to generate content after multiple attempts.")
    return None


if user_photo:
    # Görseli oku ve numpy array'e çevir
    bytes_data = user_photo.read()
    nparr = np.frombuffer(bytes_data, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Orijinal görseli göster
    st.image(img_np, channels="BGR", caption="Orijinal Kahve Fincanı")

    # Görseli gri tona çevir
    gray_img = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

    # Görüntüyü bulanıklaştır (gürültüyü azaltmak için)
    blurred_img = cv2.GaussianBlur(gray_img, (5, 5), 0)

    # Kenarları bulma (contour detection)
    edges = cv2.Canny(blurred_img, 50, 150)

    # Konturları bul
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Konturları çizin
    contour_img = img_np.copy()
    cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)

    # Konturları göster
    st.image(contour_img, caption="Kahve fincanındaki şekiller", use_column_width=True)

    # Yorumlama için bir prompt oluştur
    if len(contours) > 0:
        prompt = f"Kahve fincanında {len(contours)} adet şekil görüyorum. Bu şekiller arasında dikkat çekici olanlar bir dağ ve bir yol olabilir. 10 yıllık bir kahve falı uzmanı olarak bu şekillere dayalı olarak moral yükseltici bir fal yorumu yap."
    else:
        prompt = "Kahve fincanında belirgin bir şekil göremedim. Ama genel olarak bir sürpriz habere işaret eden semboller olabilir. Bu konuda moral verici bir fal yorumu yap."

    # API'den yanıt al
    if st.button("Fal Yorumu Al"):
        cevap = generate_response(prompt)
        if cevap:
            st.write(cevap)