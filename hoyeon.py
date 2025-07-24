import streamlit as st
import time
import random

st.subheader("⚡ 반응속도 테스트")

# 초기 상태 설정
# test_state는 앱의 현재 진행 상태를 나타냅니다:
# "initial": 시작하기 전
# "preparing": 준비 중 (랜덤 대기 시간)
# "ready_to_click": 클릭 대기 중
# "testing_complete": 테스트 완료 및 결과 표시
if "test_state" not in st.session_state:
    st.session_state.test_state = "initial"
if "start_time" not in st.session_state:
    st.session_state.start_time = 0.0
if "reaction_time" not in st.session_state:
    st.session_state.reaction_time = None
if "target_wait_end_time" not in st.session_state:
    st.session_state.target_wait_end_time = 0.0

# 1. 초기 상태: "시작하기" 버튼 표시
if st.session_state.test_state == "initial":
    if st.button("🕹 시작하기", key="start_button_initial"):
        st.session_state.test_state = "preparing"
        st.session_state.reaction_time = None # 이전 결과 초기화
        # 랜덤 대기 시간을 설정합니다. (현재 시간 + 랜덤 시간)
        st.session_state.target_wait_end_time = time.time() + random.uniform(2, 4)
        st.rerun() # 상태가 변경되었으니 즉시 새로고침하여 다음 상태로 전환

# 2. 준비 중 상태: "준비 중입니다..." 메시지 표시
elif st.session_state.test_state == "preparing":
    st.write("⏳ 준비 중입니다... 절대 클릭하지 마세요!")
    
    # 목표 대기 시간이 지났는지 확인합니다.
    if time.time() >= st.session_state.target_wait_end_time:
        st.session_state.test_state = "ready_to_click"
        st.session_state.start_time = time.time() # 클릭 대기 시작 시간 기록
        st.rerun() # 즉시 새로고침하여 클릭 대기 상태로 전환
    else:
        # 아직 대기 중이라면, 사용자에게 버튼 클릭을 막기 위해 비활성화된 더미 버튼 표시
        st.button("🚫 대기 중 (클릭 불가)", disabled=True, key="dummy_button_preparing")
        # Streamlit은 상호작용이 있을 때만 리런되므로, 이 상태에서는 주기적인 리런이 필요하지 않습니다.
        # 단, 사용자가 이 상태에서 아무것도 하지 않으면 `ready_to_click` 상태로 자동 전환되지 않고
        # 무한정 'preparing'에 머물러 있을 수 있습니다.
        # 이 문제를 해결하려면 Streamlit 외부에서 특정 시간 간격으로 리런을 트리거하거나,
        # 사용자의 다른 액션을 기다려야 합니다.
        # 하지만 Streamlit의 일반적인 동작 방식에서는 st.button 같은 위젯이 클릭되면 리런이 됩니다.
        # 이 코드의 목적은 'delay'가 끝나는 시점에 UI가 바로 변하도록 하는 것이므로,
        # 이 상태에서는 특별한 추가 `rerun()`이 없어도 됩니다.

# 3. 클릭 대기 중 상태: "지금 클릭!" 버튼 표시
elif st.session_state.test_state == "ready_to_click":
    if st.button("👆 지금 클릭!", key="click_now_button"):
        st.session_state.reaction_time = time.time() - st.session_state.start_time
        st.session_state.test_state = "testing_complete"
        st.rerun() # 테스트 완료 상태로 전환

# 4. 테스트 완료 및 결과 표시 상태
elif st.session_state.test_state == "testing_complete":
    st.success(f"🎯 당신의 반응속도는 {st.session_state.reaction_time:.3f}초입니다!")
    if st.button("🔁 다시 시작하기", key="restart_button_complete"):
        st.session_state.test_state = "initial"
        st.rerun() # 초기 상태로 돌아감
