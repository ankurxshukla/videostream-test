import psycopg2

DB_URL = 'postgres://dgtasygcbqjaml:35fd7f22844e1f60e40cf2256e6fedb0e054d2bcb3eacd5476ad879cb5630728@ec2-54-159-112-44.compute-1.amazonaws.com:5432/d4ai9acoao41u2'

def create_teacher(teacher_email, teacher_password, teacher_name, admin_password):
    if admin_password != 'admin':
        return 103
    else:
        try:
            conn = psycopg2.connect(DB_URL, sslmode='require')
        except Error as e:
            print(e)
        cr = conn.cursor()
        cr.execute(str('SELECT * FROM teacher_table WHERE email = \'%s\''%(teacher_email))).fetchone()
        row = cr.fetchone()
        if row == None:
            cr.execute(str('INSERT INTO teacher_table (email, password, full_name) VALUES (\'%s\', \'%s\', \'%s\')'%(teacher_email, teacher_password, teacher_name)))
            conn.commit()
            conn.close()
            return 105
        else:
            conn.close()
            return 104
        

def get_teachers_list(admin_password):
    teacher_id_list = []
    teacher_email_list = []
    teacher_name_list = []
    if admin_password != 'admin':
        return 103, teacher_email_list, teacher_name_list
    else:
        try:
            conn = psycopg2.connect(DB_URL, sslmode='require')
        except Error as e:
            print(e)
        cr = conn.cursor()
        cr.execute('SELECT id, email, full_name FROM teacher_table')
        rows = cr.fetchall()
        for row in rows:
            teacher_id_list.append(row[0])
            teacher_email_list.append(row[1])
            teacher_name_list.append(row[2])
        conn.close()
        return 106, teacher_id_list, teacher_email_list, teacher_name_list
    
def get_students_under_teacher(admin_password, teacher_id):
    student_email_list = []
    student_name_list = []
    if admin_password != 'admin':
        return 103, student_email_list, student_name_list
    else:
        try:
            conn = psycopg2.connect(DB_URL, sslmode='require')
        except Error as e:
            print(e)
        cr = conn.cursor()
        cr.execute(str('SELECT email, full_name FROM student_table WHERE teacher_id = \'%s\''%(teacher_id)))
        rows = cr.fetchall()
        for row in rows:
            student_email_list.append(row[0])
            student_name_list.append(row[1])
        conn.close()
        return 107, student_email_list, student_name_list

def login(teacher_email, teacher_password):
    try:
        conn = psycopg2.connect(DB_URL, sslmode='require')
    except Error as e:
        print(e)
    cr = conn.cursor()
    cr.execute(str('SELECT password FROM teacher_table WHERE email = \'%s\''%(teacher_email)))
    row = cr.fetchone()
    if(row == None):
        conn.close()
        return 110
    elif(row[0] == teacher_password):
        conn.close()
        return 112
    else:
        conn.close()
        return 111
