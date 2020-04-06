from flask import Flask, render_template, request
from opentok import OpenTok
from opentok import Roles
import time
import os
import session_db
import student_db
import teacher_db

app = Flask(__name__)
api_key = '46641862'
api_secret = '641d7983a105e26612710177756d9f09928ee090'
opentok = OpenTok(api_key, api_secret)

# Index
@app.route('/')
def func():
    return render_template('index.html')

# ROOMS DATABASE
@app.route('/create_session', methods = ["POST"])
def initialize_session():
    teacher_id = request.form['teacher_id']
    room_name = request.form['room_name']
    session = opentok.create_session()
    session_id = session.session_id
    token = session.generate_token()
    room_id = session_db.create_room(room_name, session_id, token, teacher_id)
    return {'room_name': room_name, 'session_id': session_id, 'token': token, 'teacher_id': teacher_id}

@app.route('/token', methods=['POST'])
def generate_token():
    room_id = request.form['room_id']
    result_code, room_name, room_session_id, room_teacher_id = session_db.get_room_details(room_id)
    if(result_code == 115):
        token = opentok.generate_token(room_session_id, expire_time=int(time.time() + (2 * 60 * 60)))
        return {'result_code': result_code, 'room_name': room_name, 'session_id': room_session_id, 'room_teacher_id': room_teacher_id, 'token': token}
    else:
        return {'result_code': result_code}

@app.route('/rooms')
def rooms():
    room_id_list, room_name_list, room_session_id_list, room_teacher_id_list = session_db.get_rooms_list()
    return {'room_id_list': room_id_list, 'room_name_list': room_name_list, 'room_session_id_list': room_session_id_list, 'room_teacher_id_list': room_teacher_id_list}

@app.route('/delete_session', methods=['POST'])
def delete_session():
    session_id = str(request.form['session_id'])
    result_code = session_db.delete_room(session_id)
    return result_code

@app.route('/session_details', methods=['POST'])
def session_details():
    room_id = request.form['room_id']
    room_name, session_id, teacher_id = session_db.get_room_details(room_id)
    return {'room_name': room_name, 'session_id': session_id, 'teacher_id': teacher_id}


# STUDENT DATABASE
@app.route('/create_student', methods=['POST'])
def create_student():
    student_email = request.form['student_email']
    student_password = request.form['student_password']
    student_name = request.form['student_name']
    student_teacher_id = request.form['student_teacher_id']
    student_class = request.form['student_class']
    result_code = student_db.create_student(student_email, student_password, student_name, student_teacher_id, student_class)
    return {'result_code': result_code}

@app.route('/student_login', methods=['POST'])
def initiate_student_login():
    student_email = request.form['student_email']
    student_password = request.form['student_password']
    result_code = student_db.login(student_email, student_password)
    return {'result_code': result_code}

@app.route('/student_details', methods=['POST'])
def get_student_details():
    student_email = request.form['student_email']
    student_id, student_name, student_teacher_id, student_class = student_db.get_student_details(student_email)
    return {'student_id': student_id, 'student_email': student_email, 'student_name': student_name, 'student_teacher_id': student_teacher_id, 'student_class': student_class}


# TEACHER DATABASE
@app.route('/create_teacher', methods=['POST'])
def create_teacher():
    teacher_email = request.form['teacher_email']
    teacher_password = request.form['teacher_password']
    teacher_name = request.form['teacher_name']
    admin_password = request.form['admin_password']
    result_code = teacher_db.create_teacher(teacher_email, teacher_password, teacher_name, admin_password)
    return {'result_code': result_code}

@app.route('/teacher_login', methods=['POST'])
def initiate_teacher_login():
    teacher_email = request.form['teacher_email']
    teacher_password = request.form['teacher_password']
    result_code = teacher_db.login(teacher_email, teacher_password)
    return {'result_code': result_code}

@app.route('/get_students_under_teacher', methods=['POST'])
def get_students_under_teacher():
    admin_password = request.form['admin_password']
    teacher_id = request.form['teacher_id']
    result_code,  student_email_list, student_name_list = teacher_db.get_students_under_teacher(admin_password, teacher_id)
    return {'result_code': result_code, 'student_email_list': student_email_list, 'student_name_list': student_name_list}

@app.route('/teachers_list', methods=['POST'])
def teachers_list():
    admin_password = request.form['admin_password']
    result_code, teacher_id_list, teacher_email_list, teacher_name_list = teacher_db.get_teachers_list(admin_password)
    return {'result_code': result_code, 'teacher_id_list': teacher_id_list, 'teacher_email_list': teacher_email_list, 'teacher_name_list': teacher_name_list}

if __name__ == "__main__":
    app.run(debug=True)