import streamlit as st
import subprocess
from set import load_codes


st.set_page_config(
    page_title="EdMakers GPT",
    page_icon="favicon.png",
)

# 암호 코드 로드
codes = load_codes()
user_code = codes["user_code"]
admin_code = codes["admin_code"]

st.title("에듀메이커스 Chat GPT")

# 로그인 폼
with st.form(key='login_form'):
    secret_code = st.text_input("암호 코드를 입력하세요:", type="password")
    submit_button = st.form_submit_button("확인")

    if submit_button:
        # 내가 코드 입력했음을 알리기 위한 메시지
        st.success("코드가 입력되었습니다. 필요한 페이지로 이동합니다.")

        # 코드에 따라 페이지 실행
        if secret_code == admin_code:
            subprocess.Popen(["streamlit", "run", "cod.py"])  # 관리자 페이지 실행
        elif secret_code == user_code:
            subprocess.Popen(["streamlit", "run", "new.py"])  # 사용자 페이지 실행
        else:
            st.error("잘못된 코드입니다.")  # 잘못된 코드일 경우 오류 메시지 출력
