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

st.markdown("<h1 style='text-align: center;'>에듀메이커스 Chat GPT</h1>", unsafe_allow_html=True)

# JavaScript 함수 정의
st.markdown("""
<script>
function redirect(url) {
    window.location.href = url;
}
</script>
""", unsafe_allow_html=True)

# 로그인 폼
with st.form(key='login_form'):
    secret_code = st.text_input("암호 코드를 입력하세요:", type="password")
    submit_button = st.form_submit_button("확인")

if submit_button:
    if secret_code == admin_code:
        st.success("관리자 코드가 확인되었습니다. 관리자 페이지로 이동합니다.")
        st.markdown(f'<script>redirect("https://edmakers-selectmode.streamlit.app/")</script>', unsafe_allow_html=True)
    elif secret_code == user_code:
        st.success("사용자 코드가 확인되었습니다. GPT 페이지로 이동합니다.")
        st.markdown(f'<script>redirect("https://edmakers-gpt.streamlit.app/")</script>', unsafe_allow_html=True)
    else:
        st.error("잘못된 코드입니다.")

# 페이지 하단에 이미지 추가
st.image("favicon.png", caption="EduMakers Logo", width=200)
