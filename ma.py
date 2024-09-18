import streamlit as st
import hashlib
from datetime import datetime
import sqlite3

st.set_page_config(
    page_title="EduMakers Code page",
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
    expiry_date TEXT
)
''')
conn.commit()

# 비밀번호 해시화
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# 사용자 등록 함수
def add_user(username, password, expiry_date):
    password_hash = make_hashes(password)
    expiry_date_str = expiry_date.strftime("%Y-%m-%d %H:%M:%S.%f")
    c.execute("INSERT INTO users (username, password_hash, expiry_date) VALUES (?, ?, ?)",
              (username, password_hash, expiry_date_str))
    conn.commit()

def main():
    st.title("회원가입 페이지")
    new_user = st.text_input("새 사용자 이름")
    new_password = st.text_input("새 비밀번호", type='password')
    expiry_date = st.date_input("계정 만료일 선택", value=datetime.now())

    if st.button("회원가입"):
        c.execute("SELECT username FROM users WHERE username = ?", (new_user,))
        if c.fetchone():
            st.warning("이미 존재하는 사용자 이름입니다.")
        else:
            add_user(new_user, new_password, expiry_date)
            st.success("계정이 생성되었습니다.")

if __name__ == '__main__':
    main()
