import streamlit as st
from set import load_codes

st.set_page_config(
    page_title="EdMakers Code page",
    page_icon="favicon.png",
)

# 암호 코드 로드
codes = load_codes()
user_code = codes["user_code"]
admin_code = codes["admin_code"]

# 세션 상태 초기화
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_type = None

st.markdown("<h1 style='text-align: center;'>에듀메이커스 Chat GPT</h1>", unsafe_allow_html=True)

# 인증되지 않은 경우에만 로그인 폼 표시
if not st.session_state.authenticated:
    with st.form(key='login_form'):
        secret_code = st.text_input("암호 코드를 입력하세요:", type="password")
        submit_button = st.form_submit_button("확인")

    if submit_button:
        if secret_code == admin_code:
            st.session_state.authenticated = True
            st.session_state.user_type = 'admin'
            st.experimental_rerun()
        elif secret_code == user_code:
            st.session_state.authenticated = True
            st.session_state.user_type = 'user'
            st.experimental_rerun()
        else:
            st.error("잘못된 코드입니다.")
else:
    if st.session_state.user_type == 'admin':
        st.success("관리자 코드가 확인되었습니다. 관리자 페이지로 이동합니다.")
        st.markdown("[관리자 페이지로 이동](https://edmakers-selectmode.streamlit.app/)")
    elif st.session_state.user_type == 'user':
        st.success("사용자 코드가 확인되었습니다. GPT 페이지로 이동합니다.")
        st.markdown("[GPT 페이지로 이동](https://edmakers-gpt.streamlit.app/)")
    
    if st.button("로그아웃"):
        st.session_state.authenticated = False
        st.session_state.user_type = None
        st.experimental_rerun()

# 페이지 하단에 이미지 추가
st.image("favicon.png", caption="EdMakers Logo", width=200)
