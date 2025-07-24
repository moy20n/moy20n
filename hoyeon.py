import streamlit as st
import time
import random

st.set_page_config("⚡ 반응속도 테스트", layout="centered")
st.title("⚡ 빠른 클릭 테스트")

if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "result" not in st.session_state:
    st.session_state.result = None
if "ready" not in st.session_state:
    st.session_state.ready = False

# 단계 1: 준비 버튼
if not st.session_state.ready:
    if st.button("🎯 테스트 시작하기"):
        wait_time = random.uniform(2, 5)
        st.session_state.ready = True
        st.session_state.start_time = None
        st.session_state.result = None
        st.session_state.wait_until = time.time() + wait_time
        st.experimental_rerun()

# 단계 2: 기다렸다가 버튼 표시
elif st.session_state.ready:
    now = time.time()
    if st.session_state.start_time is None:
        if now < st.session_state.wait_until:
            st.write("⏳ 준비하세요...")
            time.sleep(0.2)
            st.experimental_rerun()
        else:
            st.session_state.start_time = time.time()
            st.experimental_rerun()
    else:
        if st.button("🔥 지금 클릭!"):
            reaction_time = (time.time() - st.session_state.start_time) * 1000
            st.session_state.result = round(reaction_time)
            st.session_state.ready = False
            st.experimental_rerun()

# 결과 표시
if st.session_state.result is not None:
    st.success(f"⏱ 반응속도: {st.session_state.result}ms")
