import cv2 as cv
import gradio as gr
import numpy as np

# print("Version:", cv.__version__)
#
# # 1. Görsel İşlemleri
# # 2. Görsel Hakkında Bilgi Alma
# # 3. Gradio
#
#
# # 1. Görsel İşlemleri ###
#
# # imread fonksiyonu görseli okuyarak sayı dizisi şeklinde alır. 255 beyaz: 255 renk yoğunluğu rengi
# img = cv.imread("Project1-BackToBlack/images/satranc3x3.jpeg")
# print(img)
#
# # çıktı matris bir tablo. sütunlar ve satırlardan oluşuyor.
# # [] bir pixel , bgr için 3 farklı renk var
# # [[]] satır
# # [[[]][][]] alt alta gelerek görüntüyü oluşturuyor.
#
# # Kırmızı (Red): RGB (255, 0, 0)
# # Yeşil (Green): RGB (0, 255, 0)
# # Mavi (Blue): RGB (0, 0, 255)
# # Beyaz (White): RGB (255, 255, 255)
# # Siyah (Black): RGB (0, 0, 0)
# # Sarı (Yellow): RGB (255, 255, 0)
#
# print(img.shape) ## 600 * 600 'den oluşan bir görsel. satır/sütun/boyut
# # sayı dizisini tekrar görsel olarak görme:
# cv.imshow("Satranc 3x3", img)
# # açıp kapatıyor bekleme yapmamız lazım.
# # bekle ve klavyeden bir tuşa basıldığında çık
# cv.waitKey(0)
# cv.destroyAllWindows()
#
# #2. Görsel Hakkında Bilgi Alma ###
#
# img = cv.imread("Project1-BackToBlack/images/yesil_elma.jpeg")
#
# # shape nedir? görüntünün boyutlarını almamızı sağlar. yükseklik, genişlik.
# height,width = img.shape[:2]
# print(height,width)
# #shapedeki son parametre channel sayısını belirtir. tuple olarak döner
# channels = img.shape[-1] # or 2
# print(channels)
#
# # Farklı okuma modları
# img_file = r"Project1-BackToBlack/images/satranc3x3.jpeg"
#
# # Renkli Okuma
# img_color = cv.imread(img_file, cv.IMREAD_COLOR) #renkli olarak okuması için cv.IMREAD_COLOR yazdık
# #img_color = cv.imread(img_file, 1) 'de olur
#
# # Siyah Beyaz Okuma
# img_gray = cv.imread(img_file, cv.IMREAD_GRAYSCALE)
# #img_gray = cv.imread(img_file, 0) 'de olur
#
# cv.imshow("Renkli",img_color)
# cv.imshow("Siyah Beyaz", img_gray)
# cv.waitKey(0)
# cv.destroyAllWindows()
#
# #### Apple Photo
# img_file_2 = r"Project1-BackToBlack/images/yesil_elma.jpeg"
# img_apple_gray = cv.imread(img_file_2, cv.IMREAD_GRAYSCALE)
# cv.imshow("Gri Elma", img_apple_gray)
# cv.waitKey(0)
# cv.destroyAllWindows()

#3. Gradio ####
# gradio nedir? web tabanlı arayüz oluşturmak için kullanılan bir kütüphanedir. streamlitin kankası
#!pip install gradio

import cv2 as cv
import gradio as gr
import numpy as np

# Görseli siyah-beyaza dönüştüren fonksiyon
def nostalji(image):
    image = np.array(image)
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    return gray_image

# Gradio arayüzü oluştur
with gr.Blocks() as demo:
    gr.Markdown("# Convert Image to Black and White! ")
    gr.Markdown("Upload a photo")

    image_input = gr.Image(type='pil', label="Input Photo")

    # Bileşenleri fonksiyonla bağla
    btn = gr.Button("Convert")
    image_output = gr.Image(type="numpy", label="Output Photo")
    btn.click(fn=nostalji, inputs=image_input, outputs=image_output)

# Gradio arayüzünü başlat
if __name__ == "__main__":
    demo.launch(share=True)