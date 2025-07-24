import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw
import random
import math

st.set_page_config(page_title="🎯 과녁 맞히기", layout="centered")
st.title("🎯 과녁 클릭해서 맞히기 게임")

# 초기 세션 설정
if "score" not in st.session_state:
    st.session_state.score = 0
if "target" not in st.session_state:
    st.session_state.target = (random.randint(50, 450), random.randint(50, 450))

# 과녁 이미지 만들기
def get_canvas_with_target(x, y):
    img = Image.new("RGB", (500, 500), "white")
    draw = ImageDraw.Draw(img)
    draw.ellipse((x-20, y-20, x+20, y+20), fill="red", outline="black", width=2)
    return img

target_x, target_y = st.session_state.target
target_img = get_canvas_with_target(target_x, target_y)

st.markdown("과녁을 **직접 클릭**해보세요!")

canvas_result = st_canvas(
    fill_color="rgba(0, 0, 0, 0)",
    stroke_width=0,
    background_image=target_img,
    update_streamlit=True,
    height=500,
    width=500,
    drawing_mode="transform",  # 실제 도형은 안 그려지고 클릭 좌표만 받기 위함
    key="canvas",
)

# 클릭 판정
if canvas_result.json_data is not None:
    objects = canvas_result.json_data["objects"]
    if objects:
        last_click = objects[-1]
        click_x = last_click["left"]
        click_y = last_click["top"]
        
        # 거리 계산
        dist = math.hypot(click_x - target_x, click_y - target_y)
        if dist <= 25:
            st.session_state.score += 1
            st.success(f"🎯 명중! (+1점)")
            st.session_state.target = (random.randint(50, 450), random.randint(50, 450))
        else:
            st.warning("😢 빗나갔어요! 다시 도전!")

# 점수 출력
st.markdown(f"### 점수: **{st.session_state.score}점**")

# 리셋
if st.button("🔄 리셋"):
    st.session_state.score = 0
    st.session_state.target = (random.randint(50, 450), random.randint(50, 450))
