import streamlit as st
from set import load_codes

st.set_page_config(
    page_title="EduMakers Code page",
    page_icon="favicon.png",
)

# 암호 코드 로드
codes = load_codes()
user_code = codes["user_code"]
admin_code = codes["admin_code"]

st.markdown("<h1 style='text-align: center;'>에듀메이커스 Chat GPT</h1>", unsafe_allow_html=True)

# 로그인 폼
with st.form(key='login_form'):
    secret_code = st.text_input("암호 코드를 입력하세요:", type="password")
    submit_button = st.form_submit_button("확인")

# 폼 제출 처리 (버튼 클릭 또는 엔터 키)
if submit_button or secret_code:  # 버튼 클릭 또는 엔터 키 입력
    if secret_code == admin_code:
        st.success("관리자 코드가 확인되었습니다. 관리자 페이지로 이동합니다.")
        st.markdown("[관리자 페이지로 이동](https://edmakers-selectmode.streamlit.app/)")
    elif secret_code == user_code:
        st.success("사용자 코드가 확인되었습니다. GPT 페이지로 이동합니다.")
        st.markdown("[GPT 페이지로 이동](https://edmakers-gpt.streamlit.app/)")
    else:
        st.error("잘못된 코드입니다.")

# 페이지 하단에 이미지 추가
st.image("favicon.png", caption="EduMakers Logo")
