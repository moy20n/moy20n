import streamlit as st
import random
import time

# 앱 설정
st.set_page_config(page_title="🎮 미니게임 허브", layout="centered")
st.title("🎮 미니게임 허브에 오신 걸 환영합니다!")

# 게임 선택 메뉴
game_choice = st.selectbox("🎮 플레이할 게임을 선택하세요", [
    "🔢 업다운 게임",
    "⚡ 반응속도 테스트",
])

# 공통 초기화
if "score" not in st.session_state:
    st.session_state.score = 0

# ----------------------------
# 🔢 1. 업다운 게임
# ----------------------------
if game_choice == "🔢 업다운 게임":
    st.subheader("🔢 숫자 업다운 게임")
    if "target_number" not in st.session_state:
        st.session_state.target_number = random.randint(1, 100)
        st.session_state.tries = 0

    guess = st.number_input("1부터 100 사이의 숫자를 입력하세요", min_value=1, max_value=100, step=1)

    if st.button("제출"):
        st.session_state.tries += 1
        if guess < st.session_state.target_number:
            st.info("🔼 업! 더 큰 숫자입니다.")
        elif guess > st.session_state.target_number:
            st.info("🔽 다운! 더 작은 숫자입니다.")
        else:
            st.success(f"🎉 정답입니다! 시도 횟수: {st.session_state.tries}")
            st.session_state.target_number = random.randint(1, 100)
            st.session_state.tries = 0

# ----------------------------
# ⚡ 6. 반응속도 테스트
# ----------------------------
elif game_choice == "⚡ 반응속도 테스트":
    st.subheader("⚡ 반응속도 테스트")
    
    if "ready" not in st.session_state:
        st.session_state.ready = False
        st.session_state.start_time = 0.0

    if not st.session_state.ready:
        if st.button("🕹 시작하기"):
            st.write("🕐 준비 중... 잠시만 기다리세요!")
            wait_time = random.uniform(2, 5)
            time.sleep(wait_time)
            st.session_state.start_time = time.time()
            st.session_state.ready = True
            st.experimental_rerun()
    else:
        if st.button("👆 지금 클릭!"):
            reaction_time = time.time() - st.session_state.start_time
            st.success(f"⚡ 반응속도: {reaction_time:.3f}초")
            st.session_state.ready = False
