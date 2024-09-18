import streamlit as st
import sqlite3
import hashlib

st.set_page_config(
    page_title="EduMakers Code page",
    page_icon="favicon.png",
)

# SQLite 데이터베이스 연결 및 테이블 생성
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()

# users 테이블이 존재하지 않으면 생성
c.execute('''
    CREATE TABLE IF NOT EXISTS users
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    expiry_date TEXT)
''')
conn.commit()

# 비밀번호 해시화 함수
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def get_users():
    try:
        c.execute("SELECT id, username, password_hash, expiry_date FROM users")
        return c.fetchall()
    except sqlite3.OperationalError as e:
        st.error(f"데이터베이스 오류: {e}")
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
                  (username, password_hash, "2025-12-31 23:59:59.999999"))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    except sqlite3.Error as e:
        st.error(f"테스트 사용자 추가 중 오류 발생: {e}")
        return False

def main():
    st.title("관리자 페이지")

    # 테스트용 사용자 추가 버튼 (개발 중에만 사용)
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
            col1, col2 = st.columns([5, 1])  # 삭제 버튼의 공간을 오른쪽 끝에 배치
            with col1:
                st.markdown(f'''
                <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">
                <div>ID: {username}</div>
                <div>Password Hash: {password_hash}</div>
                <div>Expiry Date: {expiry_date}</div>
                </div>
                ''', unsafe_allow_html=True)
            with col2:
                if st.button(f"삭제", key=f"delete_{user_id}"):
                    if delete_user(user_id):
                        st.success(f"{username} 계정이 삭제되었습니다.")
                        st.experimental_rerun()  # 페이지 새로고침
                    else:
                        st.error(f"{username} 계정 삭제에 실패했습니다.")
    else:
        st.write("등록된 회원이 없거나 데이터를 불러오는 데 문제가 발생했습니다.")

if __name__ == '__main__':
    main()
