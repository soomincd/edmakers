import sqlite3

# SQLite 데이터베이스 연결
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()

# 테이블에 열이 존재하는지 확인
c.execute("PRAGMA table_info(users)")
columns = [row[1] for row in c.fetchall()]

# 열이 존재하지 않으면 추가
if 'expiry_date' not in columns:
    c.execute('ALTER TABLE users ADD COLUMN expiry_date DATE')

conn.commit()
conn.close()
