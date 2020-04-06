import sqlite3
import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(PROJECT_ROOT, 'database', 'videostream.db')
print(DATABASE)
conn = None

def create_student(student_email, student_password, student_name, student_teacher_id, student_class):
    try:
        conn = sqlite3.connect(DATABASE)
    except Error as e:
        print(e)
    cr = conn.cursor()
    cr.execute('SELECT * from student_table WHERE email = ?', [student_email])
    row = cr.fetchone()
    if(row == None):
        cr.execute('INSERT INTO student_table (email, password, full_name, teacher_id, student_class) VALUES (?, ?, ?, ?, ?)', (student_email, student_password, student_name, student_teacher_id, student_class))
        conn.commit()
        conn.close()
        return 109
    else:
        conn.close()
        return 108

def login(student_email, student_password):
    try:
        conn = sqlite3.connect(DATABASE)
    except Error as e:
        print(e)
    cr = conn.cursor()
    password = cr.execute('SELECT password FROM student_table WHERE email = ?', [student_email]).fetchone()
    if(password == None):
        conn.close()
        return 101
    elif(str(password) == str(student_password)):
        conn.close()
        return 100
    else:
        conn.close()
        return 102

def get_student_detail(student_id):
    try:
        conn = sqlite3.connect(DATABASE)
    except Error as e:
        print(e)
    cr = conn.cursor()
    cr.execute('SELECT email, full_name, teacher_id, student_class FROM student_table WHERE id = ?', [student_id])
    rows = cr.fetchone()
    conn.close()
    return rows[0], rows[1], rows[2], rows[3]
    