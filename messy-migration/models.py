from db import get_db_connection

def get_all_users():
    conn = get_db_connection()
    users = conn.execute('SELECT id, name, email FROM users').fetchall()
    conn.close()
    return users

def get_user_by_id(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT id, name, email FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return user

def get_user_by_email(email):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    return user

def create_user(name, email, password_hash):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, password_hash))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id

def update_user(user_id, name, email):
    conn = get_db_connection()
    conn.execute('UPDATE users SET name = ?, email = ? WHERE id = ?', (name, email, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

def search_users_by_name(name):
    conn = get_db_connection()
    pattern = f'%{name}%'
    users = conn.execute('SELECT id, name, email FROM users WHERE name LIKE ?', (pattern,)).fetchall()
    conn.close()
    return users
