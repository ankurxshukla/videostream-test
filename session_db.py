import psycopg2

DB_URL = 'postgres://dgtasygcbqjaml:35fd7f22844e1f60e40cf2256e6fedb0e054d2bcb3eacd5476ad879cb5630728@ec2-54-159-112-44.compute-1.amazonaws.com:5432/d4ai9acoao41u2'

def get_rooms_list():
    try:
        conn = psycopg2.connect(DB_URL, sslmode='require')
    except Error as e:
        print(e)
    cr = conn.cursor()
    query = 'SELECT * FROM rooms_table'
    cr.execute(query)
    room_id_list = []
    room_name_list = []
    room_session_id_list = []
    room_teacher_id_list = []
    rows = cr.fetchall()
    for row in rows:
        room_id_list.append(row[0])
        room_name_list.append(row[1])
        room_session_id_list.append(row[2])
        room_teacher_id_list.append(row[3])
    conn.commit()
    conn.close()
    return room_id_list, room_name_list, room_session_id_list, room_teacher_id_list

def get_room_details(room_id):
    try:
        conn = psycopg2.connect(DB_URL, sslmode='require')
    except Error as e:
        print(e)
    cr = conn.cursor()
    cr.execute(str('SELECT * FROM rooms_table WHERE id = \'%s\''%(room_id)))
    row = cr.fetchone()
    if(row != None):
        conn.close()
        return 115, row[1], row[2], row[3]
    else:
        conn.close()
        return 116, '', '', ''

def create_room(room_name, room_session_id, token, room_teacher_id):
    try:
        conn = psycopg2.connect(DB_URL, sslmode='require')
    except Error as e:
        print(e)
    cr = conn.cursor()
    cr.execute(str('INSERT INTO rooms_table (name, session_id, token, teacher_id) VALUES (\'%s\', \'%s\', \'s\', \'%s\')'%(room_name, room_session_id, token, room_teacher_id)))
    conn.commit()
    conn.close()

def delete_room(session_id):
    conn = psycopg2.connect(DB_URL, sslmode='require')
    cr = conn.cursor()
    cr.execute(str('SELECT * FROM rooms_table WHERE session_id = \'%s\''%(session_id)))
    row = cr.fetchone()
    if row != None:
        cr.execute(str('DELETE FROM rooms_table WHERE session_id = \'%s\''%(session_id)))
        conn.commit()
        conn.close()
        return 113
    else:
        conn.commit()
        conn.close()
        return 114