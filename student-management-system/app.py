"""
Student Management System - Main Application

This is the main Flask application file that serves as the controller
in the MVC architecture. It contains:
- Database models (Model layer)
- Routes and view functions (Controller layer)
- Application initialization and configuration

MVC Implementation:
- Model: Student, Course, Attendance classes define data structure and relationships
- View: Jinja2 templates in /templates directory render HTML
- Controller: Route functions handle requests, process data, and render views
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError, Optional
from config import Config
from datetime import datetime, date
from sqlalchemy import func

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db = SQLAlchemy(app)


# =============================================================================
# MODELS (Model Layer)
# =============================================================================

# Association table for many-to-many relationship between Student and Course
student_courses = db.Table('student_courses',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True)
)


class Student(db.Model):
    """Student model representing the students table."""
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    enrollment_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(20))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Many-to-many relationship with Course
    courses = db.relationship('Course', secondary=student_courses,
                              backref=db.backref('students', lazy='dynamic'))
    
    # One-to-many relationship with Attendance
    attendance_records = db.relationship('Attendance', backref='student', lazy='dynamic',
                                         cascade='all, delete-orphan')
    
    def get_full_name(self):
        """Return full name of the student."""
        return f"{self.first_name} {self.last_name}"
    
    def get_attendance_percentage(self, course_id=None):
        """Calculate attendance percentage for the student."""
        query = self.attendance_records
        if course_id:
            query = query.filter_by(course_id=course_id)
        
        total = query.count()
        if total == 0:
            return 0.0
        
        present = query.filter(Attendance.status.in_(['Present', 'Late'])).count()
        return round((present / total) * 100, 2)
    
    def __repr__(self):
        return f'<Student {self.enrollment_number}: {self.get_full_name()}>'


class Course(db.Model):
    """Course model representing the courses table."""
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    course_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    credits = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # One-to-many relationship with Attendance
    attendance_records = db.relationship('Attendance', backref='course', lazy='dynamic',
                                         cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Course {self.course_code}: {self.course_name}>'


class Attendance(db.Model):
    """Attendance model representing the attendance table."""
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False, index=True)
    attendance_date = db.Column(db.Date, nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False)  # Present, Absent, Late
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Attendance {self.student_id} - {self.course_id} on {self.attendance_date}>'


# =============================================================================
# FORMS (Form Classes for WTForms)
# =============================================================================

class StudentForm(FlaskForm):
    """Form for adding/editing students."""
    enrollment_number = StringField('Enrollment Number', validators=[
        DataRequired(message='Enrollment number is required'),
        Length(max=50, message='Enrollment number must be 50 characters or less')
    ])
    first_name = StringField('First Name', validators=[
        DataRequired(message='First name is required'),
        Length(max=100, message='First name must be 100 characters or less')
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(message='Last name is required'),
        Length(max=100, message='Last name must be 100 characters or less')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address'),
        Length(max=120, message='Email must be 120 characters or less')
    ])
    phone = StringField('Phone', validators=[
        Optional(),
        Length(max=20, message='Phone must be 20 characters or less')
    ])
    date_of_birth = DateField('Date of Birth', validators=[Optional()])
    gender = SelectField('Gender', choices=[
        ('', 'Select Gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ], validators=[Optional()])
    address = TextAreaField('Address', validators=[Optional()])
    submit = SubmitField('Save Student')
    
    def __init__(self, original_enrollment=None, original_email=None, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.original_enrollment = original_enrollment
        self.original_email = original_email
    
    def validate_enrollment_number(self, field):
        """Validate that enrollment number is unique."""
        student = Student.query.filter_by(enrollment_number=field.data).first()
        if student and student.enrollment_number != self.original_enrollment:
            raise ValidationError('Enrollment number already exists. Please use a different one.')
    
    def validate_email(self, field):
        """Validate that email is unique."""
        student = Student.query.filter_by(email=field.data).first()
        if student and student.email != self.original_email:
            raise ValidationError('Email already registered. Please use a different email.')


class CourseForm(FlaskForm):
    """Form for adding/editing courses."""
    course_code = StringField('Course Code', validators=[
        DataRequired(message='Course code is required'),
        Length(max=20, message='Course code must be 20 characters or less')
    ])
    course_name = StringField('Course Name', validators=[
        DataRequired(message='Course name is required'),
        Length(max=200, message='Course name must be 200 characters or less')
    ])
    description = TextAreaField('Description', validators=[Optional()])
    credits = IntegerField('Credits', validators=[Optional()])
    submit = SubmitField('Save Course')
    
    def __init__(self, original_code=None, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.original_code = original_code
    
    def validate_course_code(self, field):
        """Validate that course code is unique."""
        course = Course.query.filter_by(course_code=field.data).first()
        if course and course.course_code != self.original_code:
            raise ValidationError('Course code already exists. Please use a different code.')


class AttendanceForm(FlaskForm):
    """Form for marking attendance."""
    student_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    course_id = SelectField('Course', coerce=int, validators=[DataRequired()])
    attendance_date = DateField('Date', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late')
    ], validators=[DataRequired()])
    remarks = TextAreaField('Remarks', validators=[Optional()])
    submit = SubmitField('Mark Attendance')
    
    def __init__(self, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)
        # Populate student and course choices
        self.student_id.choices = [(s.id, f"{s.get_full_name()} ({s.enrollment_number})") 
                                    for s in Student.query.order_by(Student.last_name).all()]
        self.course_id.choices = [(c.id, f"{c.course_code} - {c.course_name}") 
                                   for c in Course.query.order_by(Course.course_code).all()]


class AssignCourseForm(FlaskForm):
    """Form for assigning a course to a student."""
    course_id = SelectField('Select Course', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Assign Course')
    
    def __init__(self, student_id, *args, **kwargs):
        super(AssignCourseForm, self).__init__(*args, **kwargs)
        # Get courses not already assigned to this student
        student = Student.query.get(student_id)
        if student:
            assigned_course_ids = [c.id for c in student.courses]
            available_courses = Course.query.filter(~Course.id.in_(assigned_course_ids)).all()
            self.course_id.choices = [(c.id, f"{c.course_code} - {c.course_name}") 
                                       for c in available_courses]
        else:
            self.course_id.choices = []


# =============================================================================
# CONTROLLER (Route Handlers)
# =============================================================================

@app.route('/')
def dashboard():
    """Dashboard route - displays overview statistics."""
    # Get counts
    total_students = Student.query.count()
    total_courses = Course.query.count()
    total_attendance = Attendance.query.count()
    
    # Get recent students (last 5)
    recent_students = Student.query.order_by(Student.created_at.desc()).limit(5).all()
    
    # Get students with low attendance (below 75%)
    low_attendance_students = []
    all_students = Student.query.all()
    for student in all_students:
        percentage = student.get_attendance_percentage()
        if percentage < 75 and percentage > 0:  # Only include if they have some attendance records
            low_attendance_students.append({
                'student': student,
                'percentage': percentage
            })
    
    return render_template('dashboard.html',
                         total_students=total_students,
                         total_courses=total_courses,
                         total_attendance=total_attendance,
                         recent_students=recent_students,
                         low_attendance_students=low_attendance_students)


# -------------------------
# Student Routes
# -------------------------

@app.route('/students')
def students_list():
    """List all students with search functionality."""
    search_query = request.args.get('search', '')
    course_filter = request.args.get('course', '', type=int)
    
    query = Student.query
    
    # Search by name, email, or enrollment number
    if search_query:
        search_term = f"%{search_query}%"
        query = query.filter(
            (Student.first_name.ilike(search_term)) |
            (Student.last_name.ilike(search_term)) |
            (Student.email.ilike(search_term)) |
            (Student.enrollment_number.ilike(search_term))
        )
    
    # Filter by course
    if course_filter:
        query = query.filter(Student.courses.any(id=course_filter))
    
    students = query.order_by(Student.last_name, Student.first_name).all()
    courses = Course.query.order_by(Course.course_code).all()
    
    return render_template('students/list.html', students=students, courses=courses,
                         search_query=search_query, course_filter=course_filter)


@app.route('/students/add', methods=['GET', 'POST'])
def student_add():
    """Add a new student."""
    form = StudentForm()
    
    if form.validate_on_submit():
        student = Student(
            enrollment_number=form.enrollment_number.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone.data,
            date_of_birth=form.date_of_birth.data,
            gender=form.gender.data,
            address=form.address.data
        )
        
        try:
            db.session.add(student)
            db.session.commit()
            flash(f'Student {student.get_full_name()} added successfully!', 'success')
            return redirect(url_for('students_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding student: {str(e)}', 'danger')
    
    return render_template('students/form.html', form=form, title='Add Student', edit=False)


@app.route('/students/<int:id>')
def student_detail(id):
    """View student details including courses and attendance."""
    student = Student.query.get_or_404(id)
    
    # Calculate overall attendance percentage
    attendance_percentage = student.get_attendance_percentage()
    
    # Get attendance history
    attendance_records = Attendance.query.filter_by(student_id=id)\
        .order_by(Attendance.attendance_date.desc()).all()
    
    # Get all courses for assignment dropdown
    all_courses = Course.query.order_by(Course.course_code).all()
    
    return render_template('students/detail.html', student=student,
                         attendance_percentage=attendance_percentage,
                         attendance_records=attendance_records,
                         all_courses=all_courses,
                         courses_count=len(all_courses))


@app.route('/students/<int:id>/edit', methods=['GET', 'POST'])
def student_edit(id):
    """Edit an existing student."""
    student = Student.query.get_or_404(id)
    form = StudentForm(original_enrollment=student.enrollment_number, 
                       original_email=student.email)
    
    if request.method == 'GET':
        # Pre-populate form fields
        form.enrollment_number.data = student.enrollment_number
        form.first_name.data = student.first_name
        form.last_name.data = student.last_name
        form.email.data = student.email
        form.phone.data = student.phone
        form.date_of_birth.data = student.date_of_birth
        form.gender.data = student.gender
        form.address.data = student.address
    
    if form.validate_on_submit():
        student.enrollment_number = form.enrollment_number.data
        student.first_name = form.first_name.data
        student.last_name = form.last_name.data
        student.email = form.email.data
        student.phone = form.phone.data
        student.date_of_birth = form.date_of_birth.data
        student.gender = form.gender.data
        student.address = form.address.data
        
        try:
            db.session.commit()
            flash(f'Student {student.get_full_name()} updated successfully!', 'success')
            return redirect(url_for('student_detail', id=student.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating student: {str(e)}', 'danger')
    
    return render_template('students/form.html', form=form, title='Edit Student', 
                         edit=True, student=student)


@app.route('/students/<int:id>/delete', methods=['POST'])
def student_delete(id):
    """Delete a student."""
    student = Student.query.get_or_404(id)
    
    try:
        db.session.delete(student)
        db.session.commit()
        flash(f'Student {student.get_full_name()} deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting student: {str(e)}', 'danger')
    
    return redirect(url_for('students_list'))


@app.route('/students/<int:id>/assign-course', methods=['POST'])
def assign_course(id):
    """Assign a course to a student."""
    student = Student.query.get_or_404(id)
    form = AssignCourseForm(student_id=id)
    
    if form.validate_on_submit():
        course = Course.query.get(form.course_id.data)
        if course:
            if course not in student.courses:
                student.courses.append(course)
                try:
                    db.session.commit()
                    flash(f'Course {course.course_code} assigned to {student.get_full_name()}!', 'success')
                except Exception as e:
                    db.session.rollback()
                    flash(f'Error assigning course: {str(e)}', 'danger')
            else:
                flash('Student is already enrolled in this course.', 'warning')
        else:
            flash('Course not found.', 'danger')
    else:
        for error in form.errors.values():
            flash(error[0], 'danger')
    
    return redirect(url_for('student_detail', id=id))


@app.route('/students/<int:id>/remove-course/<int:course_id>', methods=['POST'])
def remove_course(id, course_id):
    """Remove a course assignment from a student."""
    student = Student.query.get_or_404(id)
    course = Course.query.get_or_404(course_id)
    
    if course in student.courses:
        student.courses.remove(course)
        try:
            db.session.commit()
            flash(f'Course {course.course_code} removed from {student.get_full_name()}!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error removing course: {str(e)}', 'danger')
    else:
        flash('Student was not enrolled in this course.', 'warning')
    
    return redirect(url_for('student_detail', id=id))


# -------------------------
# Course Routes
# -------------------------

@app.route('/courses')
def courses_list():
    """List all courses."""
    courses = Course.query.order_by(Course.course_code).all()
    return render_template('courses/list.html', courses=courses)


@app.route('/courses/add', methods=['GET', 'POST'])
def course_add():
    """Add a new course."""
    form = CourseForm()
    
    if form.validate_on_submit():
        course = Course(
            course_code=form.course_code.data,
            course_name=form.course_name.data,
            description=form.description.data,
            credits=form.credits.data
        )
        
        try:
            db.session.add(course)
            db.session.commit()
            flash(f'Course {course.course_code} added successfully!', 'success')
            return redirect(url_for('courses_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding course: {str(e)}', 'danger')
    
    return render_template('courses/form.html', form=form, title='Add Course', edit=False)


@app.route('/courses/<int:id>/edit', methods=['GET', 'POST'])
def course_edit(id):
    """Edit an existing course."""
    course = Course.query.get_or_404(id)
    form = CourseForm(original_code=course.course_code)
    
    if request.method == 'GET':
        form.course_code.data = course.course_code
        form.course_name.data = course.course_name
        form.description.data = course.description
        form.credits.data = course.credits
    
    if form.validate_on_submit():
        course.course_code = form.course_code.data
        course.course_name = form.course_name.data
        course.description = form.description.data
        course.credits = form.credits.data
        
        try:
            db.session.commit()
            flash(f'Course {course.course_code} updated successfully!', 'success')
            return redirect(url_for('courses_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating course: {str(e)}', 'danger')
    
    return render_template('courses/form.html', form=form, title='Edit Course', 
                         edit=True, course=course)


@app.route('/courses/<int:id>/delete', methods=['POST'])
def course_delete(id):
    """Delete a course."""
    course = Course.query.get_or_404(id)
    
    try:
        db.session.delete(course)
        db.session.commit()
        flash(f'Course {course.course_code} deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting course: {str(e)}', 'danger')
    
    return redirect(url_for('courses_list'))


# -------------------------
# Attendance Routes
# -------------------------

@app.route('/attendance')
def attendance_list():
    """List attendance records with filtering options."""
    student_filter = request.args.get('student', '', type=int)
    course_filter = request.args.get('course', '', type=int)
    date_filter = request.args.get('date', '')
    
    query = Attendance.query
    
    if student_filter:
        query = query.filter_by(student_id=student_filter)
    
    if course_filter:
        query = query.filter_by(course_id=course_filter)
    
    if date_filter:
        try:
            date_obj = datetime.strptime(date_filter, '%Y-%m-%d').date()
            query = query.filter_by(attendance_date=date_obj)
        except ValueError:
            pass
    
    attendance_records = query.order_by(Attendance.attendance_date.desc()).all()
    students = Student.query.order_by(Student.last_name).all()
    courses = Course.query.order_by(Course.course_code).all()
    
    return render_template('attendance/list.html', 
                         attendance_records=attendance_records,
                         students=students,
                         courses=courses,
                         student_filter=student_filter,
                         course_filter=course_filter,
                         date_filter=date_filter)


@app.route('/attendance/mark', methods=['GET', 'POST'])
def attendance_mark():
    """Mark attendance for a student."""
    form = AttendanceForm()
    
    # Set default date to today
    if request.method == 'GET':
        from datetime import date
        form.attendance_date.data = date.today()
    
    if form.validate_on_submit():
        # Check if attendance already exists for this student/course/date
        existing = Attendance.query.filter_by(
            student_id=form.student_id.data,
            course_id=form.course_id.data,
            attendance_date=form.attendance_date.data
        ).first()
        
        if existing:
            flash('Attendance already marked for this student on this date for this course.', 'warning')
        else:
            attendance = Attendance(
                student_id=form.student_id.data,
                course_id=form.course_id.data,
                attendance_date=form.attendance_date.data,
                status=form.status.data,
                remarks=form.remarks.data
            )
            
            try:
                db.session.add(attendance)
                db.session.commit()
                flash('Attendance marked successfully!', 'success')
                return redirect(url_for('attendance_list'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error marking attendance: {str(e)}', 'danger')
    
    return render_template('attendance/mark.html', form=form)


# =============================================================================
# Error Handlers
# =============================================================================

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return render_template('error.html', error_code=404, 
                         message='The page you are looking for does not exist.'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    db.session.rollback()
    return render_template('error.html', error_code=500, 
                         message='An internal server error occurred.'), 500


# =============================================================================
# Database Initialization
# =============================================================================

def create_tables():
    """Create database tables."""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")


def seed_data():
    """Insert sample data for testing."""
    with app.app_context():
        # Check if data already exists
        if Student.query.first():
            print("Sample data already exists. Skipping seed.")
            return
        
        # Create sample students
        students = [
            Student(
                enrollment_number='ENG2024001',
                first_name='John',
                last_name='Doe',
                email='john.doe@college.edu',
                phone='555-0101',
                date_of_birth=date(2002, 5, 15),
                gender='Male',
                address='123 Main St, Cityville'
            ),
            Student(
                enrollment_number='ENG2024002',
                first_name='Jane',
                last_name='Smith',
                email='jane.smith@college.edu',
                phone='555-0102',
                date_of_birth=date(2001, 8, 22),
                gender='Female',
                address='456 Oak Ave, Townsburg'
            ),
            Student(
                enrollment_number='ENG2024003',
                first_name='Bob',
                last_name='Johnson',
                email='bob.johnson@college.edu',
                phone='555-0103',
                date_of_birth=date(2002, 3, 10),
                gender='Male',
                address='789 Pine Rd, Villagetown'
            ),
            Student(
                enrollment_number='ENG2024004',
                first_name='Alice',
                last_name='Williams',
                email='alice.williams@college.edu',
                phone='555-0104',
                date_of_birth=date(2001, 11, 5),
                gender='Female',
                address='321 Elm St, Hamletville'
            ),
            Student(
                enrollment_number='ENG2024005',
                first_name='Charlie',
                last_name='Brown',
                email='charlie.brown@college.edu',
                phone='555-0105',
                date_of_birth=date(2002, 7, 18),
                gender='Male',
                address='654 Maple Dr, Boroughton'
            ),
        ]
        
        # Create sample courses
        courses = [
            Course(
                course_code='CS101',
                course_name='Introduction to Computer Science',
                description='Fundamentals of computer science and programming',
                credits=3
            ),
            Course(
                course_code='CS201',
                course_name='Data Structures',
                description='Study of data structures and algorithms',
                credits=4
            ),
            Course(
                course_code='MATH101',
                course_name='Calculus I',
                description='Introduction to differential and integral calculus',
                credits=4
            ),
            Course(
                course_code='ENG101',
                course_name='English Composition',
                description='Writing and composition skills',
                credits=3
            ),
            Course(
                course_code='PHY101',
                course_name='Physics I',
                description='Mechanics and thermodynamics',
                credits=4
            ),
        ]
        
        db.session.add_all(students)
        db.session.add_all(courses)
        db.session.commit()
        
        # Assign courses to students
        students[0].courses.append(courses[0])  # John -> CS101
        students[0].courses.append(courses[1])  # John -> CS201
        students[0].courses.append(courses[2])  # John -> MATH101
        
        students[1].courses.append(courses[0])  # Jane -> CS101
        students[1].courses.append(courses[2])  # Jane -> MATH101
        students[1].courses.append(courses[3])  # Jane -> ENG101
        
        students[2].courses.append(courses[1])  # Bob -> CS201
        students[2].courses.append(courses[4])  # Bob -> PHY101
        
        students[3].courses.append(courses[0])  # Alice -> CS101
        students[3].courses.append(courses[3])  # Alice -> ENG101
        
        students[4].courses.append(courses[2])  # Charlie -> MATH101
        students[4].courses.append(courses[4])  # Charlie -> PHY101
        
        db.session.commit()
        
        # Add sample attendance records
        today = date.today()
        attendance_data = [
            # John's attendance
            {'student_id': 1, 'course_id': 1, 'days_ago': 1, 'status': 'Present'},
            {'student_id': 1, 'course_id': 1, 'days_ago': 2, 'status': 'Present'},
            {'student_id': 1, 'course_id': 1, 'days_ago': 3, 'status': 'Late'},
            {'student_id': 1, 'course_id': 1, 'days_ago': 4, 'status': 'Present'},
            {'student_id': 1, 'course_id': 1, 'days_ago': 5, 'status': 'Absent'},
            {'student_id': 1, 'course_id': 2, 'days_ago': 1, 'status': 'Present'},
            {'student_id': 1, 'course_id': 2, 'days_ago': 2, 'status': 'Present'},
            {'student_id': 1, 'course_id': 2, 'days_ago': 3, 'status': 'Present'},
            
            # Jane's attendance
            {'student_id': 2, 'course_id': 1, 'days_ago': 1, 'status': 'Present'},
            {'student_id': 2, 'course_id': 1, 'days_ago': 2, 'status': 'Present'},
            {'student_id': 2, 'course_id': 1, 'days_ago': 3, 'status': 'Present'},
            {'student_id': 2, 'course_id': 1, 'days_ago': 4, 'status': 'Present'},
            {'student_id': 2, 'course_id': 3, 'days_ago': 1, 'status': 'Absent'},
            {'student_id': 2, 'course_id': 3, 'days_ago': 2, 'status': 'Absent'},
            {'student_id': 2, 'course_id': 3, 'days_ago': 3, 'status': 'Late'},
            
            # Bob's attendance (low attendance)
            {'student_id': 3, 'course_id': 2, 'days_ago': 1, 'status': 'Absent'},
            {'student_id': 3, 'course_id': 2, 'days_ago': 2, 'status': 'Absent'},
            {'student_id': 3, 'course_id': 2, 'days_ago': 3, 'status': 'Present'},
            {'student_id': 3, 'course_id': 5, 'days_ago': 1, 'status': 'Absent'},
            {'student_id': 3, 'course_id': 5, 'days_ago': 2, 'status': 'Late'},
            
            # Alice's attendance
            {'student_id': 4, 'course_id': 1, 'days_ago': 1, 'status': 'Present'},
            {'student_id': 4, 'course_id': 1, 'days_ago': 2, 'status': 'Present'},
            {'student_id': 4, 'course_id': 1, 'days_ago': 3, 'status': 'Present'},
            {'student_id': 4, 'course_id': 1, 'days_ago': 4, 'status': 'Present'},
            {'student_id': 4, 'course_id': 4, 'days_ago': 1, 'status': 'Present'},
            {'student_id': 4, 'course_id': 4, 'days_ago': 2, 'status': 'Late'},
            
            # Charlie's attendance (very low attendance)
            {'student_id': 5, 'course_id': 3, 'days_ago': 1, 'status': 'Absent'},
            {'student_id': 5, 'course_id': 3, 'days_ago': 2, 'status': 'Absent'},
            {'student_id': 5, 'course_id': 3, 'days_ago': 3, 'status': 'Absent'},
            {'student_id': 5, 'course_id': 5, 'days_ago': 1, 'status': 'Present'},
        ]
        
        for record in attendance_data:
            attendance = Attendance(
                student_id=record['student_id'],
                course_id=record['course_id'],
                attendance_date=today.replace(day=today.day - record['days_ago']) if today.day > record['days_ago'] else today,
                status=record['status'],
                remarks='Sample attendance record'
            )
            db.session.add(attendance)
        
        db.session.commit()
        print("Sample data seeded successfully!")


# =============================================================================
# Application Entry Point
# =============================================================================

if __name__ == '__main__':
    # Create tables and seed data
    create_tables()
    seed_data()
    
    # Run the application
    print("\n" + "="*60)
    print("Student Management System")
    print("="*60)
    print("Starting server at http://127.0.0.1:5000")
    print("Press CTRL+C to quit")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
