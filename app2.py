from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random string
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    subjects = db.Column(db.String(200), nullable=False)  # Comma-separated subjects

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    scores = db.Column(db.Integer, nullable=False)
    attendance = db.Column(db.String(105), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email_mobile = db.Column(db.String(120), nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    user_type = request.form['user_type']
    id_input = request.form['id']
    password = request.form['password']

    if user_type == 'teacher':
        teacher = Teacher.query.filter_by(teacher_id=id_input, password=password).first()
        if teacher:
            session['user_id'] = teacher.id
            session['user_type'] = 'teacher'
            return redirect(url_for('teacher_dashboard'))
        else:
            flash('Invalid ID or password!')
            return redirect(url_for('index'))
    elif user_type == 'student':
        student = Student.query.filter_by(student_id=id_input, password=password).first()
        if student:
            session['user_id'] = student.id
            session['user_type'] = 'student'
            return redirect(url_for('student'))
        else:
            flash('Invalid ID or password! If not added by a teacher, contact them.')
            return redirect(url_for('index'))

@app.route('/register_teacher', methods=['GET', 'POST'])
def register_teacher():
    if request.method == 'POST':
        teacher_id = request.form['teacher_id']
        name = request.form['name']
        gender = request.form['gender']
        mobile = request.form['mobile']
        email = request.form['email']
        password = request.form['password']
        subjects = ','.join(request.form.getlist('subjects'))

        new_teacher = Teacher(teacher_id=teacher_id, name=name, gender=gender, mobile=mobile,
                              email=email, password=password, subjects=subjects)
        db.session.add(new_teacher)
        db.session.commit()
        flash('Teacher registered successfully!')
        return redirect(url_for('index'))
    return render_template('register_teacher.html')

@app.route('/teacher_dashboard', methods=['GET', 'POST'])
def teacher_dashboard():
    if 'user_type' not in session or session['user_type'] != 'teacher':
        return redirect(url_for('index'))

    students = Student.query.all()

    if request.method == 'POST':
        action = request.form.get('action')
        print(f"Action: {action}, Form Data: {request.form}")  # Debug print
        if action == 'add':
            student_id = request.form['student_id']
            name = request.form['name']
            age = request.form['age']
            gender = request.form['gender']
            course = request.form['course']
            scores = request.form['scores']
            attendance = request.form['attendance']
            password = request.form['password']
            email_mobile = request.form['email_mobile']

            new_student = Student(student_id=student_id, name=name, age=age, gender=gender,
                                course=course, scores=scores, attendance=attendance, password=password, email_mobile=email_mobile)
            db.session.add(new_student)
            db.session.commit()
            flash('Student added successfully!')
        elif action == 'update':
            student_id = request.form['student_id']
            student = Student.query.filter_by(student_id=student_id).first()
            if student:
                student.name = request.form['name']
                student.age = int(request.form['age'])  # Ensure age is an integer
                student.gender = request.form['gender']
                student.course = request.form['course']
                student.scores = int(request.form['scores'])
                student.attendance = request.form['attendance']
                student.password = request.form['password']
                student.email_mobile = request.form['email_mobile']
                db.session.commit()
                flash('Student details updated successfully!')
            else:
                flash('Student not found!')
        elif action == 'delete':
            student_id = request.form['student_id']
            student = Student.query.filter_by(student_id=student_id).first()
            if student:
                db.session.delete(student)
                db.session.commit()
                flash('Student removed successfully!')

    return render_template('teacher_dashboard.html', students=students)

@app.route('/edit_student/<student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    if 'user_type' not in session or session['user_type'] != 'teacher':
        return redirect(url_for('index'))

    student = Student.query.filter_by(student_id=student_id).first()
    if not student:
        flash('Student not found!')
        return redirect(url_for('teacher_dashboard'))

    if request.method == 'POST':
        student.name = request.form['name']
        student.age = int(request.form['age'])
        student.gender = request.form['gender']
        student.course = request.form['course']
        student.scores = int(request.form['scores'])
        student.attendance = request.form['attendance']
        student.password = request.form['password']
        student.email_mobile = request.form['email_mobile']
        db.session.commit()
        flash('Student details updated successfully!')
        return redirect(url_for('teacher_dashboard'))

    return render_template('edit_student.html', student=student)

@app.route('/student')
def student():
    if 'user_type' not in session or session['user_type'] != 'student':
        return redirect(url_for('index'))
    
    student = Student.query.get(session['user_id'])
    return render_template('student.html', student=student)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_type', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)