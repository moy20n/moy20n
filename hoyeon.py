import streamlit as st
import random
import time

st.set_page_config(page_title="🎮 미니게임 허브", layout="centered")
st.title("🎮 미니게임 허브에 오신 걸 환영합니다!")

game_choice = st.selectbox("게임을 선택하세요!", [
    "🔢 업다운 게임",
    "⚡ 반응속도 테스트",
    "🧠 기억력 테스트",
    "🧮 빠른 계산 게임"
])

# 공통 초기화
if "score" not in st.session_state:
    st.session_state.score = 0

# ----------------------------
# 🔢 업다운 게임
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
# ⚡ 반응속도 테스트
# ----------------------------
elif game_choice == "⚡ 반응속도 테스트":
    st.subheader("⚡ 반응속도 테스트")

    if "reaction_state" not in st.session_state:
        st.session_state.reaction_state = "ready"
        st.session_state.start_time = None
        st.session_state.reaction_time = None

    if st.session_state.reaction_state == "ready":
        if st.button("🕹 시작하기"):
            st.session_state.reaction_state = "waiting"
            st.session_state.wait_start_time = time.time()
            st.session_state.wait_duration = random.uniform(2, 5)
            st.experimental_rerun()

    elif st.session_state.reaction_state == "waiting":
        if time.time() - st.session_state.wait_start_time < st.session_state.wait_duration:
            st.write("⏳ 준비 중... 기다리세요!")
            time.sleep(0.1)
            st.experimental_rerun()
        else:
            st.session_state.reaction_state = "now"
            st.session_state.start_time = time.time()
            st.experimental_rerun()

    elif st.session_state.reaction_state == "now":
        st.success("🎯 지금 클릭하세요!")
        if st.button("👆 클릭!"):
            reaction_time = time.time() - st.session_state.start_time
            st.success(f"⚡ 반응속도: {reaction_time:.3f}초")
            st.session_state.reaction_state = "result"
            st.session_state.reaction_time = reaction_time

    elif st.session_state.reaction_state == "result":
        st.write(f"⚡ 당신의 반응속도: **{st.session_state.reaction_time:.3f}초**")
        if st.button("🔄 다시 도전하기"):
            for key in ["reaction_state", "start_time", "reaction_time", "wait_start_time", "wait_duration"]:
                st.session_state.pop(key, None)
            st.experimental_rerun()

# ----------------------------
# 🧠 기억력 테스트
# ----------------------------
elif game_choice == "🧠 기억력 테스트":
    st.subheader("🧠 기억력 테스트")

    if "memory_numbers" not in st.session_state:
        st.session_state.memory_numbers = []
        st.session_state.input_numbers = []
        st.session_state.showing = False
        st.session_state.correct = None

    def generate_numbers():
        st.session_state.memory_numbers = [random.randint(0, 9) for _ in range(4)]
        st.session_state.input_numbers = []
        st.session_state.correct = None
        st.session_state.showing = True

    if st.button("🧠 숫자 보여줘!"):
        generate_numbers()
        st.experimental_rerun()

    if st.session_state.showing:
        st.write("👀 숫자를 외우세요:")
        st.markdown(f"### {'  '.join(map(str, st.session_state.memory_numbers))}")
        time.sleep(2)
        st.session_state.showing = False
        st.experimental_rerun()

    if not st.session_state.showing and st.session_state.memory_numbers:
        st.write("💡 숫자를 순서대로 입력하세요:")
        cols = st.columns(len(st.session_state.memory_numbers))
        for i in range(len(st.session_state.memory_numbers)):
            with cols[i]:
                st.session_state.input_numbers.append(
                    st.number_input(f"{i+1}", min_value=0, max_value=9, step=1, key=f"mem_input_{i}")
                )

        if st.button("제출하기"):
            if st.session_state.input_numbers == st.session_state.memory_numbers:
                st.success("🎉 정답입니다! 대단한 기억력!")
                st.session_state.correct = True
            else:
                st.error("❌ 틀렸어요! 다시 도전해보세요.")
                st.session_state.correct = False

# ----------------------------
# 🧮 빠른 계산 게임
# ----------------------------
elif game_choice == "🧮 빠른 계산 게임":
    st.subheader("🧮 10초 동안 수학 문제 풀기")

    if "calc_start" not in st.session_state:
        st.session_state.calc_start = None
        st.session_state.calc_score = 0
        st.session_state.calc_question = ""
        st.session_state.calc_answer = 0

    def new_calc_question():
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        op = random.choice(["+", "-", "*"])
        question = f"{a} {op} {b}"
        answer = eval(question)
        return question, answer

    if st.button("🕐 시작하기"):
        st.session_state.calc_start = time.time()
        st.session_state.calc_score = 0
        q, a = new_calc_question()
        st.session_state.calc_question = q
        st.session_state.calc_answer = a

    if st.session_state.calc_start:
        elapsed = time.time() - st.session_state.calc_start
        if elapsed > 10:
            st.success(f"⏰ 시간 종료! 정답 수: {st.session_state.calc_score}")
            st.session_state.calc_start = None
        else:
            st.write(f"남은 시간: {10 - int(elapsed)}초")
            st.markdown(f"### 문제: {st.session_state.calc_question}")
            user_answer = st.number_input("정답 입력", step=1, key="calc_input")
            if st.button("제출", key="calc_submit"):
                if int(user_answer) == st.session_state.calc_answer:
                    st.success("정답!")
                    st.session_state.calc_score += 1
                else:
                    st.error("오답!")
                q, a = new_calc_question()
                st.session_state.calc_question = q
                st.session_state.calc_answer = a
                st.experimental_rerun()

