import streamlit as st
from PIL import Image, ImageDraw
import requests
from io import BytesIO
import time
import random

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

# 在圖片上添加手掌效果
def add_hands_effect(image):
    draw = ImageDraw.Draw(image)
    # 假設圖片中心為 (0, 0)，將 (-1, 1) 轉換為像素位置
    width, height = image.size
    center_x, center_y = width // 2, height // 2
    hand_x = center_x - int(width * 0.1)  # 向左偏移 10%
    hand_y = center_y - int(height * 0.1)  # 向上偏移 10%

    # 繪製手掌形狀（矩形與圓弧結合）
    draw.ellipse((hand_x - 30, hand_y - 30, hand_x + 30, hand_y + 30), fill="brown", outline="black")  # 手掌圓心
    draw.rectangle((hand_x - 50, hand_y - 10, hand_x - 30, hand_y + 40), fill="brown", outline="black")  # 左手指
    draw.rectangle((hand_x + 30, hand_y - 10, hand_x + 50, hand_y + 40), fill="brown", outline="black")  # 右手指
    return image

# 添加動態不規則白色噴射效果
def add_water_effect(image):
    width, height = image.size
    frames = []

    for i in range(20):  # 20 幀對應約 5 秒
        frame = image.copy()
        draw = ImageDraw.Draw(frame)
        # 動態多條不規則水線效果
        for _ in range(random.randint(3, 6)):  # 隨機生成 3 到 6 條水線
            start_x = random.randint(0, width)
            start_y = random.randint(height // 2, height)
            end_x = start_x + random.randint(-50, 50)
            end_y = start_y - random.randint(50, 150)
            draw.line((start_x, start_y, end_x, end_y), fill="white", width=random.randint(2, 5))
            draw.ellipse((end_x - 5, end_y - 5, end_x + 5, end_y + 5), fill="white")
        frames.append(frame)
    return frames

# Streamlit 網頁標題
st.title("圖片特效選擇程式")

# 提供選擇選項
st.write("請選擇以下效果：")
option = st.selectbox("選擇效果 (A 或 B)：", ("A - 摸胸肌效果", "B - YY 噴射效果"))

# 測試圖片是否加載成功
st.write(f"Image A loaded: {image_a is not None}")
st.write(f"Image B loaded: {image_b is not None}")

# 根據選擇顯示結果
if option == "A - 摸胸肌效果" and image_a is not None:
    st.subheader("你選擇了：摸胸肌效果")
    result_image = add_hands_effect(image_a.copy())
    st.image(result_image, caption="已添加摸胸肌效果", use_column_width=True)

elif option == "B - YY 噴射效果" and image_b is not None:
    st.subheader("你選擇了：YY 噴射效果")
    frames = add_water_effect(image_b.copy())
    placeholder = st.empty()  # 創建一個可動態更新的容器
    for frame in frames:
        placeholder.image(frame, use_column_width=True)
        time.sleep(0.25)  # 模擬動畫效果
