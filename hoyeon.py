import streamlit as st
import random
import time
from PIL import Image, ImageDraw

st.set_page_config("🎯 과녁 게임 허브", layout="centered")
st.title("🎯 과녁 맞히기 게임 허브")

# 모드 선택
mode = st.selectbox("🎮 게임 모드를 선택하세요", ["기본 모드", "제한 시간 모드", "과녁 축소 모드", "리액션 모드"])

# 공통 상태 초기화
if "score" not in st.session_state:
    st.session_state.score = 0

# 각 모드별 동작
if mode == "기본 모드":
    st.subheader("🔹 버튼을 눌러 과녁을 맞히세요!")
    if "target" not in st.session_state:
        st.session_state.target = (random.randint(50, 450), random.randint(50, 450))

    def draw_target(x, y, size=40):
        img = Image.new("RGB", (500, 500), "white")
        draw = ImageDraw.Draw(img)
        draw.ellipse((x-size, y-size, x+size, y+size), fill="red", outline="black")
        return img

    x, y = st.session_state.target
    img = draw_target(x, y)
    st.image(img)

    if st.button("🎯 맞히기"):
        st.session_state.score += 1
        st.session_state.target = (random.randint(50, 450), random.randint(50, 450))
        st.success("명중!")

    st.write(f"점수: {st.session_state.score}점")

elif mode == "제한 시간 모드":
    st.subheader("⏱ 30초 안에 최대한 많이 맞히세요!")
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()
        st.session_state.score = 0

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, 30 - elapsed)
    st.write(f"⏱ 남은 시간: {remaining}초")

    if "target" not in st.session_state:
        st.session_state.target = (random.randint(50, 450), random.randint(50, 450))

    x, y = st.session_state.target
    img = draw_target(x, y)
    st.image(img)

    if remaining > 0 and st.button("🎯 맞히기"):
        st.session_state.score += 1
        st.session_state.target = (random.randint(50, 450), random.randint(50, 450))

    if remaining <= 0:
        st.success(f"⏰ 시간 종료! 당신의 점수는 {st.session_state.score}점입니다.")
        if st.button("🔄 다시 시작"):
            st.session_state.start_time = time.time()
            st.session_state.score = 0
            st.session_state.target = (random.randint(50, 450), random.randint(50, 450))

elif mode == "과녁 축소 모드":
    st.subheader("👀 과녁이 점점 작아져요!")
    if "target" not in st.session_state:
        st.session_state.target = (random.randint(50, 450), random.randint(50, 450))
    if "target_size" not in st.session_state:
        st.session_state.target_size = 40

    x, y = st.session_state.target
    size = st.session_state.target_size
    img = draw_target(x, y, size=size)
    st.image(img)

    if st.button("🎯 맞히기"):
        st.session_state.score += 1
        st.session_state.target = (random.randint(50, 450), random.randint(50, 450))
        st.session_state.target_size = max(10, size - 2)

    st.write(f"점수: {st.session_state.score}점 / 과녁 크기: {st.session_state.target_size}px")

elif mode == "리액션 모드":
    st.subheader("⚡ 빠르게 반응해서 과녁을 맞히세요!")
    if "target" not in st.session_state:
        st.session_state.target = (random.randint(50, 450), random.randint(50, 450))
    if "target_time" not in st.session_state:
        st.session_state.target_time = time.time()

    x, y = st.session_state.target
    img = draw_target(x, y)
    st.image(img)

    if st.button("🎯 맞히기"):
        reaction_time = round(time.time() - st.session_state.target_time, 2)
        st.success(f"🎯 명중! 반응속도: {reaction_time}초")
        st.session_state.score += max(0, int(10 - reaction_time * 10))
        st.session_state.target = (random.randint(50, 450), random.randint(50, 450))
        st.session_state.target_time = time.time()

    st.write(f"점수: {st.session_state.score}점")

