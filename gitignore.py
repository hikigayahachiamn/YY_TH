import streamlit as st
from PIL import Image, ImageDraw
import requests
from io import BytesIO
import time
import random

# Google Drive 圖片 URL（轉換為直接下載格式）
url_a = "https://drive.google.com/uc?export=download&id=1ZMkNBHG2HF9WsJVw2OdpltGBpyg2HJX4"
url_b = "https://drive.google.com/uc?export=download&id=1I-Hh8vgS4-f9spCHmcqY8rHJxzwtb_84"
url_c = "https://drive.google.com/uc?export=download&id=1g0TBjO1J5EyvhcmYjlL9B24eVKMO1bTG"
url_hand = "https://drive.google.com/uc?export=download&id=1RwSpl9CzH2TtxNS6gNuZAovrVe17YnM0"
url_c_overlay = "https://drive.google.com/uc?export=download&id=1ef5JbC9k87oSsYKPzPcpWCfLbYV6yZHY"

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
image_c = load_image_from_url(url_c)
hand_image = load_image_from_url(url_hand)
c_overlay_image = load_image_from_url(url_c_overlay)

# A 模式：將手掌圖片疊加到目標圖片上，並調整固定大小
def add_overlay_image(background_image, overlay_image, position, size):
    background = background_image.convert("RGBA")
    overlay_resized = overlay_image.resize(size)  # 調整疊加圖片大小
    background.paste(overlay_resized, position, overlay_resized)
    return background

# B 模式：添加動態不規則白色噴射效果
def add_water_effect(image):
    width, height = image.size
    frames = []
    for i in range(20):  # 20 幀動畫
        frame = image.copy()
        draw = ImageDraw.Draw(frame)
        for _ in range(random.randint(3, 6)):
            start_x = random.randint(0, width)
            start_y = random.randint(height // 2, height)
            end_x = start_x + random.randint(-50, 50)
            end_y = start_y - random.randint(50, 150)
            draw.line((start_x, start_y, end_x, end_y), fill="white", width=random.randint(6, 10))
            draw.ellipse((end_x - 5, end_y - 5, end_x + 5, end_y + 5), fill="white")
        frames.append(frame)
    return frames

# C 模式：將指定圖片疊加到目標圖片上，並調整固定大小
def add_c_overlay(background_image, overlay_image, size):
    position = (background_image.width // 2 - size[0] // 2, background_image.height // 2 + 50)
    return add_overlay_image(background_image, overlay_image, position, size)

# Streamlit 網頁標題
st.title("子恆專屬圖片特效程式")

# 提供選擇選項
st.write("請選擇以下效果：")
option = st.selectbox(
    "選擇效果：",
    ("摸子恆胸肌", "顏設子恆", "請子恆吃基基")
)

# 根據選擇顯示結果
if option == "摸子恆胸肌" and image_a is not None and hand_image is not None:
    if st.button("顯示摸子恆胸肌效果"):
        st.subheader("你選擇了：摸子恆胸肌")
        result_image = add_overlay_image(image_a.copy(), hand_image, 
                                         position=(image_a.width // 2 - 75, image_a.height // 2 - 75), 
                                         size=(150, 150))  # 固定大小
        st.image(result_image, caption="已添加摸子恆胸肌效果", use_column_width=True)

elif option == "顏設子恆" and image_b is not None:
    if st.button("開始顏設子恆效果"):
        st.subheader("你選擇了：顏設子恆")
        frames = add_water_effect(image_b.copy())
        placeholder = st.empty()
        for frame in frames:
            placeholder.image(frame, use_column_width=True)
            time.sleep(0.25)

elif option == "請子恆吃基基" and image_c is not None and c_overlay_image is not None:
    if st.button("顯示請子恆吃基基效果"):
        st.subheader("你選擇了：請子恆吃基基")
        result_image = add_c_overlay(image_c.copy(), c_overlay_image, size=(100, 100))  # 固定大小
        st.image(result_image, caption="已顯示請子恆吃基基效果", use_column_width=True)
