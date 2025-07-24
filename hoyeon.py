import streamlit as st
import time
import random

st.set_page_config("⚡ 빠른 클릭 테스트", layout="centered")
st.title("⚡ 반응속도 테스트")

# 세션 상태 초기화
if "stage" not in st.session_state:
    st.session_state.stage = "ready"  # ready, waiting, click
if "start_time" not in st.session_state:
    st.session_state.start_time = 0.0
if "reaction_time" not in st.session_state:
    st.session_state.reaction_time = None
if "wait_until" not in st.session_state:
    st.session_state.wait_until = 0.0

# 시작 화면
if st.session_state.stage == "ready":
    st.session_state.reaction_time = None
    if st.button("🎯 테스트 시작하기"):
        wait_sec = random.uniform(2, 5)
        st.session_state.wait_until = time.time() + wait_sec
        st.session_state.stage = "waiting"
        st.experimental_rerun()

# 대기 화면
elif st.session_state.stage == "waiting":
    if time.time() < st.session_state.wait_until:
        st.write("⏳ 준비 중입니다... 기다리세요...")
        time.sleep(0.1)
        st.experimental_rerun()
    else:
        st.session_state.start_time = time.time()
        st.session_state.stage = "click"
        st.experimental_rerun()

# 클릭 화면
elif st.session_state.stage == "click":
    if st.button("🔥 지금 클릭!"):
        reaction = (time.time() - st.session_state.start_time) * 1000  # ms
        st.session_state.reaction_time = round(reaction)
        st.session_state.stage = "ready"
        st.experimental_rerun()

# 결과 표시
if st.session_state.reaction_time is not None:
    st.success(f"⏱ 당신의 반응속도는 {st.session_state.reaction_time}ms입니다!")
