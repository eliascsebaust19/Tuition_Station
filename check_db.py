import sqlite3
conn = sqlite3.connect('e:/Level 2 term II/DBMS/tuition_system/instance/tuition.db')
cur = conn.cursor()
cur.execute("SELECT id, name, profile_picture FROM users WHERE role = 'teacher' ORDER BY id")
for row in cur.fetchall():
    print(row)
conn.close()
