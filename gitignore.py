import streamlit as st
from PIL import Image, ImageDraw
import requests
from io import BytesIO

# Google Drive 圖片 URL（轉換為直接下載格式）
url_a = "https://drive.google.com/uc?export=download&id=1ZMkNBHG2HF9WsJVw2OdpltGBpyg2HJX4"
url_b = "https://drive.google.com/uc?export=download&id=1I-Hh8vgS4-f9spCHmcqY8rHJxzwtb_84"

# 從網路加載圖片
def load_image_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except requests.RequestException:
        st.error("圖片加載失敗！請檢查 URL 或網路連接。")
        return None

# 加載圖片
image_a = load_image_from_url(url_a)
image_b = load_image_from_url(url_b)

# 在胸肌上畫手的效果
def add_hands_effect(image):
    draw = ImageDraw.Draw(image)
    draw.ellipse((100, 150, 200, 250), fill="red")  # 第一隻手
    draw.ellipse((250, 150, 350, 250), fill="red")  # 第二隻手
    return image

# 添加白色水噴射效果
def add_water_effect(image):
    draw = ImageDraw.Draw(image)
    draw.line((150, 100, 200, 300), fill="white", width=15)  # 水柱
    draw.ellipse((190, 90, 210, 110), fill="white")  # 噴射點
    return image

# Streamlit 網頁標題
st.title("圖片特效選擇程式")

# 提供選擇選項
st.write("請選擇以下效果：")
option = st.selectbox("選擇效果 (A 或 B)：", ("A - 摸胸肌效果", "B - YY 噴射效果"))

# 根據選擇顯示結果
if option == "A - 摸胸肌效果" and image_a is not None:
    st.subheader("你選擇了：摸胸肌效果")
    result_image = add_hands_effect(image_a.copy())
    st.image(result_image, caption="已添加摸胸肌效果", use_column_width=True)

elif option == "B - YY 噴射效果" and image_b is not None:
    st.subheader("你選擇了：YY 噴射效果")
    result_image = add_water_effect(image_b.copy())
    st.image(result_image, caption="已添加噴射效果", use_column_width=True)
