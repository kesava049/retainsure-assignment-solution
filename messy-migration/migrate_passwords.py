import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute("SELECT id, password FROM users")
users = cursor.fetchall()

for user_id, plain_password in users:
    hashed = generate_password_hash(plain_password)
    cursor.execute("UPDATE users SET password = ? WHERE id = ?", (hashed, user_id))

conn.commit()
conn.close()

print("All existing passwords have been hashed.")
