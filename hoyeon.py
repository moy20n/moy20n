import streamlit as st
import random
import time
from PIL import Image, ImageDraw

# 세션 상태 초기화
if "score" not in st.session_state:
    st.session_state.score = 0
if "target_pos" not in st.session_state:
    st.session_state.target_pos = (random.randint(50, 450), random.randint(50, 450))
if "last_click_time" not in st.session_state:
    st.session_state.last_click_time = time.time()

st.set_page_config(page_title="🎯 과녁 맞히기 게임", layout="centered")
st.title("🎯 과녁 맞히기 게임")
st.caption("랜덤 위치에 생기는 과녁을 찾아 맞히세요! (단순 클릭 기반)")

# 이미지 생성 함수
def draw_target(x, y):
    img = Image.new("RGB", (500, 500), "white")
    draw = ImageDraw.Draw(img)
    # 과녁은 빨간색 원으로 표현
    draw.ellipse((x - 20, y - 20, x + 20, y + 20), fill="red", outline="black")
    return img

# 현재 과녁 위치에 이미지 그리기
x, y = st.session_state.target_pos
img = draw_target(x, y)
st.image(img, caption="과녁 위치를 기억하세요!", use_column_width=False)

# 클릭 버튼
if st.button("🎯 과녁 맞히기!"):
    now = time.time()
    if now - st.session_state.last_click_time < 1.0:
        st.warning("너무 빨리 클릭했어요! 😅")
    else:
        st.session_state.score += 1
        st.session_state.target_pos = (random.randint(50, 450), random.randint(50, 450))
        st.session_state.last_click_time = now
        st.success("명중! 🎯 과녁이 새 위치로 이동했어요!")

st.markdown(f"### 🔢 점수: **{st.session_state.score}점**")

# 리셋
if st.button("🔄 게임 리셋"):
    st.session_state.score = 0
    st.session_state.target_pos = (random.randint(50, 450), random.randint(50, 450))
    st.success("점수가 초기화됐어요!")

