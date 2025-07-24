elif game_choice == "⚡ 반응속도 테스트":
    st.subheader("⚡ 반응속도 테스트")

    if "reaction_state" not in st.session_state:
        st.session_state.reaction_state = "ready"
        st.session_state.start_time = None
        st.session_state.reaction_time = None

    # 상태: 시작 대기
    if st.session_state.reaction_state == "ready":
        if st.button("🕹 시작하기"):
            st.session_state.reaction_state = "waiting"
            st.session_state.wait_start_time = time.time()
            st.session_state.wait_duration = random.uniform(2, 5)
            st.experimental_rerun()
            st.stop()  # 🔒 rerun 이후 실행 중단

    # 상태: 준비 중
    elif st.session_state.reaction_state == "waiting":
        elapsed = time.time() - st.session_state.wait_start_time
        if elapsed < st.session_state.wait_duration:
            st.write("⏳ 준비 중... 손 떼고 있어요!")
            time.sleep(0.1)
            st.experimental_rerun()
            st.stop()  # 🔒 안전하게 멈춤
        else:
            st.session_state.reaction_state = "now"
            st.experimental_rerun()
            st.stop()

    # 상태: 클릭 타이밍
    elif st.session_state.reaction_state == "now":
        st.success("🎯 지금 클릭하세요!")
        if st.button("👆 클릭!"):
            st.session_state.reaction_time = time.time() - st.session_state.start_time
            st.session_state.reaction_state = "result"
            st.experimental_rerun()
            st.stop()

    # 상태: 결과 표시
    elif st.session_state.reaction_state == "result":
        st.write(f"⚡ 당신의 반응속도: **{st.session_state.reaction_time:.3f}초**")
        if st.button("🔄 다시 도전하기"):
            for key in [
                "reaction_state", "start_time", "reaction_time",
                "wait_start_time", "wait_duration"
            ]:
                st.session_state.pop(key, None)
            st.experimental_rerun()
            st.stop()
