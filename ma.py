import streamlit as st
import sqlite3
import os
import hashlib
from datetime import datetime

# 데이터베이스 초기화 및 검증 함수
def init_db():
    db_path = 'users.db'
    
    def create_table(conn):
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS users
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        expiry_date TEXT)
        ''')
        conn.commit()

    # 데이터베이스 파일이 존재하는 경우
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path, check_same_thread=False)
            # 테이블 존재 여부 확인
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            if c.fetchone() is None:
                create_table(conn)
            return conn, c
        except sqlite3.DatabaseError:
            st.warning("데이터베이스 파일이 손상되었습니다. 새로운 데이터베이스를 생성합니다.")
            os.remove(db_path)
    
    # 새 데이터베이스 생성
    conn = sqlite3.connect(db_path, check_same_thread=False)
    create_table(conn)
    return conn, conn.cursor()

# 전역 변수로 연결 객체 설정
try:
    conn, c = init_db()
except sqlite3.Error as e:
    st.error(f"데이터베이스 초기화 중 오류 발생: {e}")
    st.stop()

# 비밀번호 해시화 함수
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# 사용자 등록 함수
def add_user(username, password, expiry_date):
    password_hash = make_hashes(password)
    try:
        c.execute("INSERT INTO users (username, password_hash, expiry_date) VALUES (?, ?, ?)",
                  (username, password_hash, expiry_date.strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    except sqlite3.Error as e:
        st.error(f"사용자 추가 중 오류 발생: {e}")
        return False

def main():
    st.title("회원가입 페이지")
    
    new_user = st.text_input("새 사용자 이름")
    new_password = st.text_input("새 비밀번호", type='password')
    expiry_date = st.date_input("계정 만료일 선택", value=datetime.now())
    
    if st.button("회원가입"):
        if add_user(new_user, new_password, expiry_date):
            st.success("계정이 생성되었습니다.")
        else:
            st.warning("이미 존재하는 사용자 이름이거나 계정 생성에 실패했습니다.")

if __name__ == '__main__':
    main()
