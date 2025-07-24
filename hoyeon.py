import streamlit as st
import random
import os

st.set_page_config("🧠 끝말잇기 마스터 버전", layout="centered")
st.title("🧠 끝말잇기 챌린지 (풀옵션)")

# ✅ 대형 단어 리스트 로드
@st.cache_data
def load_words():
    path = "korean_vocab_5965.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            words = [line.strip() for line in f if len(line.strip()) >= 2]
            return list(set(words))
    else:
        return ["사과", "과자", "자동차", "차표", "표정", "정보"]  # fallback

word_list = load_words()

# ✅ 상태 초기화
if "turn" not in st.session_state:
    st.session_state.last_word = random.choice(word_list)
    st.session_state.used_words = [st.session_state.last_word]
    st.session_state.game_over = False
    st.session_state.turn = "player"
    st.session_state.result_message = ""
    st.session_state.memo = []

# ✅ 상태 표시
st.markdown(f"**🗣️ 이전 단어:** `{st.session_state.last_word}`")
st.markdown(f"[📖 `{st.session_state.last_word}` 뜻 보기](https://dic.daum.net/search.do?q={st.session_state.last_word})")
st.markdown(f"**🔁 현재 턴:** `{ '👤 당신' if st.session_state.turn == 'player' else '💻 컴퓨터' }`")

# ✅ 플레이어 차례
if not st.session_state.game_over and st.session_state.turn == "player":
    user_word = st.text_input("✏️ 다음 단어를 입력하세요").strip()

    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("✅ 제출하기"):
            if not user_word:
                st.warning("❗ 단어를 입력해주세요.")
            elif user_word in st.session_state.used_words:
                st.error("⚠️ 이미 사용된 단어입니다.")
                st.session_state.result_message = "💻 컴퓨터 승리! 중복된 단어."
                st.session_state.game_over = True
            elif user_word[0] != st.session_state.last_word[-1]:
                st.error(f"❌ 첫 글자가 `{st.session_state.last_word[-1]}` 이어야 해요.")
                st.session_state.result_message = "💻 컴퓨터 승리! 시작 글자 오류."
                st.session_state.game_over = True
            elif user_word not in word_list:
                st.error("📕 단어 사전에 없는 단어입니다.")
                st.session_state.result_message = "💻 컴퓨터 승리! 단어 없음."
                st.session_state.game_over = True
            else:
                st.success("⭕ 올바른 단어입니다!")
                st.session_state.used_words.append(user_word)
                st.session_state.last_word = user_word
                st.session_state.turn = "computer"
                st.experimental_rerun()
    with col2:
        if st.button("📝 이 단어 모르겠어요"):
            if user_word and user_word not in st.session_state.memo:
                st.session_state.memo.append(user_word)
                st.info("✅ 메모장에 저장했어요!")

# ✅ 컴퓨터 차례
elif not st.session_state.game_over and st.session_state.turn == "computer":
    st.info("💻 컴퓨터가 단어를 생각 중입니다...")
    last_char = st.session_state.last_word[-1]
    candidates = [w for w in word_list if w[0] == last_char and w not in st.session_state.used_words]

    if candidates:
        computer_word = random.choice(candidates)
        st.session_state.used_words.append(computer_word)
        st.session_state.last_word = computer_word
        st.session_state.turn = "player"
        st.success(f"💻 컴퓨터의 단어: `{computer_word}`")
        st.markdown(f"[📖 `{computer_word}` 뜻 보기](https://dic.daum.net/search.do?q={computer_word})")
    else:
        st.success("🎉 당신의 승리입니다! 컴퓨터가 단어를 못 찾았어요.")
        st.session_state.result_message = "🎉 당신 승리! 컴퓨터가 포기했어요."
        st.session_state.game_over = True

# ✅ 게임 종료 처리
if st.session_state.game_over:
    st.markdown("## 🎊 게임 종료")
    st.info(st.session_state.result_message)

    if st.button("🔄 다시 시작하기"):
        st.session_state.last_word = random.choice(word_list)
        st.session_state.used_words = [st.session_state.last_word]
        st.session_state.game_over = False
        st.session_state.turn = "player"
        st.session_state.result_message = ""
        st.experimental_rerun()

# ✅ 메모장 보기 + 저장
if st.session_state.memo:
    st.markdown("### 📒 내가 모르는 단어 메모장")
    for m in st.session_state.memo:
        st.markdown(f"- [📖 {m} 뜻 보기](https://dic.daum.net/search.do?q={m})")

    st.download_button(
        label="📥 메모장 저장 (.txt)",
        data="\n".join(st.session_state.memo),
        file_name="my_word_memo.txt",
        mime="text/plain"
    )
