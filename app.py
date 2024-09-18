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
   
# 중앙 정렬된 제목
st.markdown("<h1 style='text-align: center;'>에듀메이커스 Chat GPT</h1>", unsafe_allow_html=True)

# 로그인 폼
with st.form(key='login_form'):
    secret_code = st.text_input("암호 코드를 입력하세요:", type="password")
    submit_button = st.form_submit_button("확인")

if submit_button:
    # 내가 코드 입력했음을 알리기 위한 메시지
    st.success("코드가 입력되었습니다. 필요한 페이지로 이동합니다.")
    
    # 코드에 따라 페이지 실행
    if secret_code == admin_code:
        st.markdown("[관리자 페이지로 이동](https://edmakers-selectmode.streamlit.app/)")
    elif secret_code == user_code:
        st.markdown("[GPT 페이지로 이동](https://edmakers-gpt.streamlit.app/)")
    else:
        st.error("잘못된 코드입니다.")  # 잘못된 코드일 경우 오류 메시지 출력

# 이미지를 중앙에 배치
col1, col2, col3 = st.columns([2,2,1])
with col2:
    st.image("favicon.png", width=200)
 
