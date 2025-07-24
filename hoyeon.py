import streamlit as st
import time
import random

st.subheader("⚡ 반응속도 테스트")

# 상태 초기화
if "test_started" not in st.session_state:
    st.session_state.test_started = False
if "can_click" not in st.session_state:
    st.session_state.can_click = False
if "start_time" not in st.session_state:
    st.session_state.start_time = 0.0
if "reaction_time" not in st.session_state:
    st.session_state.reaction_time = None

# 버튼: 시작하기
if not st.session_state.test_started:
    if st.button("🕹 시작하기"):
        st.session_state.test_started = True
        st.session_state.reaction_time = None
        st.experimental_rerun()

# 상태: 시작 후 대기 → 클릭 가능 상태로 전환
elif st.session_state.test_started and not st.session_state.can_click:
    st.write("⏳ 준비 중입니다... 절대 클릭하지 마세요!")
    time.sleep(random.uniform(2, 4))  # 랜덤 대기 시간
    st.session_state.start_time = time.time()
    st.session_state.can_click = True
    st.experimental_rerun()

# 상태: 클릭 대기 중
elif st.session_state.can_click:
    if st.button("👆 지금 클릭!"):
        st.session_state.reaction_time = time.time() - st.session_state.start_time
        st.session_state.test_started = False
        st.session_state.can_click = False
        st.experimental_rerun()

# 결과 표시
if st.session_state.reaction_time is not None:
    st.success(f"🎯 당신의 반응속도는 {st.session_state.reaction_time:.3f}초입니다!")

    if st.button("🔁 다시 시작하기"):
        st.session_state.test_started = False
        st.session_state.can_click = False
        st.session_state.reaction_time = None
        st.experimental_rerun()
