import streamlit as st
import sqlite3
import hashlib
import os

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

def get_users():
    try:
        c.execute("SELECT id, username, password_hash, expiry_date FROM users")
        return c.fetchall()
    except sqlite3.Error as e:
        st.error(f"사용자 정보 조회 중 오류 발생: {e}")
        return []

def delete_user(user_id):
    try:
        c.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        st.error(f"사용자 삭제 중 오류 발생: {e}")
        return False

# 테스트용 사용자 추가 함수
def add_test_user(username, password):
    password_hash = make_hashes(password)
    try:
        c.execute("INSERT INTO users (username, password_hash, expiry_date) VALUES (?, ?, ?)", 
                  (username, password_hash, "2025-12-31"))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    except sqlite3.Error as e:
        st.error(f"테스트 사용자 추가 중 오류 발생: {e}")
        return False

def main():
    st.title("관리자 페이지")

    # 테스트용 사용자 추가 버튼
    if st.button("테스트 사용자 추가"):
        if add_test_user("testuser", "password123"):
            st.success("테스트 사용자가 추가되었습니다.")
        else:
            st.warning("테스트 사용자 추가에 실패했습니다.")

    # 사용자 목록 표시
    users = get_users()
    if users:
        for user in users:
            user_id, username, password_hash, expiry_date = user
            # 사용자 정보 표시
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f'''
                <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">
                <div>ID: {username}</div>
                <div>Password Hash: {password_hash}</div>
                <div>Expiry Date: {expiry_date or 'Not set'}</div>
                </div>
                ''', unsafe_allow_html=True)
            with col2:
                if st.button(f"삭제", key=f"delete_{user_id}"):
                    if delete_user(user_id):
                        st.success(f"{username} 계정이 삭제되었습니다.")
                        st.experimental_rerun()
                    else:
                        st.error(f"{username} 계정 삭제에 실패했습니다.")
    else:
        st.write("등록된 회원이 없거나 데이터를 불러오는 데 문제가 발생했습니다.")

if __name__ == '__main__':
    main()
