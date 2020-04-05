import sqlite3
import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(PROJECT_ROOT, 'database', 'videostream.db')
conn = None

def get_rooms_list():
    try:
        conn = sqlite3.connect(DATABASE)
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
        conn = sqlite3.connect(DATABASE)
    except Error as e:
        print(e)
    cr = conn.cursor()
    cr.execute('SELECT * FROM rooms_table WHERE id = ?', str(room_id))
    row = cr.fetchone()
    if(row != None):
        conn.close()
        return 115, row[1], row[2], row[3]
    else:
        conn.close()
        return 116, '', '', ''

def create_room(room_name, room_session_id, room_teacher_id):
    try:
        conn = sqlite3.connect(DATABASE)
    except Error as e:
        print(e)
    cr = conn.cursor()
    cr.execute('INSERT INTO rooms_table (name, session_id, teacher_id) VALUES (?, ?, ?);', (room_name, room_session_id, room_teacher_id))
    conn.commit()
    conn.close()

def delete_room(room_id):
    conn = sqlite3.connect(DATABASE)
    cr = conn.cursor()
    row = cr.execute('SELECT * FROM rooms_table WHERE id = ?', [room_id]).fetchone()
    if row != None:
        cr.execute('DELETE FROM rooms_table WHERE id = ?', [room_id])
        conn.commit()
        conn.close()
        return 113
    else:
        conn.commit()
        conn.close()
        return 114