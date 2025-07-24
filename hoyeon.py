import streamlit as st
import time
import random

st.set_page_config("⚡ 반응속도 테스트", layout="centered")
st.title("⚡ 반응속도 테스트")

# 상태 초기화
if "stage" not in st.session_state:
    st.session_state.stage = "ready"
if "start_time" not in st.session_state:
    st.session_state.start_time = 0.0
if "reaction_time" not in st.session_state:
    st.session_state.reaction_time = None
if "wait_time" not in st.session_state:
    st.session_state.wait_time = 0.0
if "trigger" not in st.session_state:
    st.session_state.trigger = False

# 단계 1: 준비
if st.session_state.stage == "ready":
    st.session_state.reaction_time = None
    if st.button("🎯 테스트 시작하기"):
        st.session_state.wait_time = random.uniform(2, 5)
        st.session_state.stage = "waiting"
        st.session_state.trigger = False
        st.experimental_rerun()

# 단계 2: 기다리기 (타이머 없이 버튼으로 진행)
elif st.session_state.stage == "waiting":
    st.info("⏳ 준비 중입니다... 버튼이 활성화되면 누르세요.")
    if not st.session_state.trigger:
        if st.button("🤫 기다리기"):
            st.session_state.trigger = True
            st.session_state.start_time = time.time()
            st.session_state.stage = "click"
            st.experimental_rerun()

# 단계 3: 클릭
elif st.session_state.stage == "click":
    if st.button("🔥 지금 클릭!"):
        reaction = (time.time() - st.session_state.start_time) * 1000
        st.session_state.reaction_time = round(reaction)
        st.session_state.stage = "ready"
        st.experimental_rerun()

# 결과 표시
if st.session_state.reaction_time is not None:
    st.success(f"⏱ 당신의 반응속도는 {st.session_state.reaction_time}ms입니다!")
