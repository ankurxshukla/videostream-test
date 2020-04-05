import sqlite3
conn = sqlite3.connect('videostream.db')
query_student_table = '''CREATE TABLE student_table (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT NOT NULL,
                        password TEXT NOT NULL,
                        full_name TEXT NOT NULL,
                        teacher_id INTEGER NOT NULL,
                        student_class TEXT NOT NULL
                        )'''

query_teacher_table = '''CREATE TABLE teacher_table (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT NOT NULL,
                        password TEXT NOT NULL,
                        full_name TEXT NOT NULL
                        )'''

query_doubts_table = '''CREATE TABLE doubts_table (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        body TEXT NOT NULL,
                        date_created TIMESTAMP,
                        student_id INTEGER NOT NULL
                        )'''

query_replies_table = '''CREATE TABLE replies_table (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        doubt_id INTEGER NOT NULL,
                        body TEXT NOT NULL,
                        date_created TIMESTAMP,
                        type BOOLEAN,
                        user_id INTEGER NOT NULL
                        )'''

query_rooms_table = '''CREATE TABLE rooms_table (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        session_id TEXT NOT NULL,
                        teacher_id INTEGER NOT NULL
                        )'''

c = conn.cursor()
c.execute(query_student_table)
c.execute(query_teacher_table)
c.execute(query_doubts_table)
c.execute(query_replies_table)
c.execute(query_rooms_table)
# c.execute('DROP TABLE student_table')
conn.commit()
conn.close()