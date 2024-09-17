import json
import streamlit as st

st.set_page_config(
    page_title="EduMakers Code page",
    page_icon="favicon.png",
)
# 암호 코드를 저장하는 함수
def save_codes(user_code, admin_code):
    codes = {
        "user_code": user_code,
        "admin_code": admin_code
    }
    with open('codes.json', 'w') as f:
        json.dump(codes, f)

# 암호 코드를 불러오는 함수
def load_codes():
    try:
        with open('codes.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # 기본 값 설정 (기본값 설정)
        return {"user_code": "5678", "admin_code": "1234"}

# Streamlit 애플리케이션 설정
st.title("암호 변경 페이지")

# 현재 암호 로드
codes = load_codes()
current_user_code = codes["user_code"]
current_admin_code = codes["admin_code"]

new_admin_code = st.text_input("새 관리자 코드를 입력하세요:", value=current_admin_code)
new_user_code = st.text_input("사용자 코드를 입력하세요:", value=current_user_code)

if st.button("변경"):
    save_codes(new_user_code, new_admin_code)
    st.success(f"관리자 코드는 {new_admin_code}, 사용자 코드는 {new_user_code}로 변경되었습니다.")

st.markdown("### 현재 암호:")
st.markdown(f"- 관리자 코드: {current_admin_code}")
st.markdown(f"- 사용자 코드: {current_user_code}")