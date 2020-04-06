import psycopg2

DB_URL = 'postgres://dgtasygcbqjaml:35fd7f22844e1f60e40cf2256e6fedb0e054d2bcb3eacd5476ad879cb5630728@ec2-54-159-112-44.compute-1.amazonaws.com:5432/d4ai9acoao41u2'

def create_student(student_email, student_password, student_name, student_teacher_id, student_class):
    try:
        conn = psycopg2.connect(DB_URL, sslmode='require')
    except Error as e:
        print(e)
    cr = conn.cursor()
    cr.execute(str('SELECT * FROM student_table WHERE email = \'%s\''%(student_email)))
    row = cr.fetchone()
    if(row == None):
        cr.execute(str('INSERT INTO student_table (email, password, full_name, teacher_id, student_class) VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\')'%(student_email, student_password, student_name, student_teacher_id, student_class)))
        conn.commit()
        conn.close()
        return 109
    else:
        conn.close()
        return 108

def login(student_email, student_password):
    try:
        conn = psycopg2.connect(DB_URL, sslmode='require')
    except Error as e:
        print(e)
    cr = conn.cursor()
    cr.execute(str('SELECT password FROM student_table WHERE email = \'%s\''%(student_email)))
    row = cr.fetchone()
    password = row[0]
    if(password == None):
        conn.close()
        return 101
    elif(password == student_password):
        conn.close()
        return 100
    else:
        conn.close()
        return 102

def get_student_detail(student_id):
    try:
        conn = psycopg2.connect(DB_URL, sslmode='require')
    except Error as e:
        print(e)
    cr = conn.cursor()
    cr.execute('SELECT email, full_name, teacher_id, student_class FROM student_table WHERE id = ?', [student_id])
    rows = cr.fetchone()
    conn.close()
    return rows[0], rows[1], rows[2], rows[3]
    