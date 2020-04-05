import sqlite3
import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(PROJECT_ROOT, 'database', 'videostream.db')
conn = None

def create_teacher(teacher_email, teacher_password, teacher_name, admin_password):
    if admin_password != 'admin':
        return False, 103
    else:
        try:
            conn = sqlite3.connect(DATABASE)
        except Error as e:
            print(e)
        cr = conn.cursor()
        row = cr.execute('SELECT * FROM teacher_table WHERE email = ?', [teacher_email]).fetchone()
        if row == None:
            cr.execute('INSERT INTO teacher_table (email, password, full_name) VALUES (?, ?, ?)', [teacher_email, teacher_password, teacher_name])
            conn.commit()
            conn.close()
            return True, 105
        else:
            conn.close()
            return False, 104
        

def get_teachers_list(admin_password):
    teacher_id_list = []
    teacher_email_list = []
    teacher_name_list = []
    if admin_password != 'admin':
        return False, 103, teacher_email_list, teacher_name_list
    else:
        try:
            conn = sqlite3.connect(DATABASE)
        except Error as e:
            print(e)
        cr = conn.cursor()
        rows = cr.execute('SELECT id, email, full_name FROM teacher_table')
        for row in rows:
            teacher_id_list.append(row[0])
            teacher_email_list.append(row[1])
            teacher_name_list.append(row[2])
        return True, 106, teacher_id_list, teacher_email_list, teacher_name_list
    
def get_students_under_teacher(admin_password, teacher_id):
    student_email_list = []
    student_name_list = []
    if admin_password != 'admin':
        return False, 103, student_email_list, student_name_list
    else:
        try:
            conn = sqlite3.connect(DATABASE)
        except Error as e:
            print(e)
        cr = conn.cursor()
        rows = cr.execute('SELECT email, full_name FROM student_table WHERE teacher_id = ?', [teacher_id])
        for row in rows:
            student_email_list.append(row[0])
            student_name_list.append(row[1])
        return True, 107, student_email_list, student_name_list

def login(teacher_email, teacher_password):
    try:
        conn = sqlite3.connect(DATABASE)
    except Error as e:
        print(e)
    cr = conn.cursor()
    password = cr.execute('SELECT password FROM student_table WHERE email = ?', [teacher_email]).fetchone()
    if(password == None):
        conn.close()
        return False, 110
    elif(password == teacher_password):
        conn.close()
        return True, 112
    else:
        conn.close()
        return False, 111
