import streamlit as st
import hashlib
from datetime import datetime
import sqlite3
import subprocess

st.set_page_config(
    page_title="EdMakers GPT",
    page_icon="favicon.png",
)

# SQLite 데이터베이스 연결
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()

# 사용자 테이블 생성 (한 번만 실행)
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password_hash TEXT,
    expiry_date DATE
)
''')
conn.commit()

# 비밀번호 해시화
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# 비밀번호 검증 
def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

# 사용자 정보 확인
def login_user(username, password):
    c.execute("SELECT password_hash, expiry_date FROM users WHERE username = ?", (username,))
    result = c.fetchone()

    if result:
        stored_password_hash, expiry_date = result
        if check_hashes(password, stored_password_hash):
            if datetime.strptime(expiry_date, "%Y-%m-%d %H:%M:%S.%f") > datetime.now():
                return "로그인 성공", expiry_date
            else:
                return "계정이 만료되었습니다", None
        else:
            return "비밀번호가 잘못되었습니다", None
    else:
        return "사용자를 찾을 수 없습니다", None

def main():
    st.title("로그인 페이지")

    username = st.text_input("사용자 이름")
    password = st.text_input("비밀번호", type='password')

    if st.button("로그인"):
        message, expiry_date = login_user(username, password)
        if message == "로그인 성공":
            st.success("올바른 코드입니다. 관리자 페이지로 이동합니다.")
            st.markdown("[GPT 페이지로 이동](https://edmakers-gpt.streamlit.app/)")
        else:
            st.error(message)

if __name__ == '__main__':
    main()
