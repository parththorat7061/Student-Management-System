# Student Management System

A comprehensive web-based application for managing student records, courses, and attendance tracking. Built with Flask, SQLAlchemy, and Bootstrap.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)

## 📋 Features

### Dashboard
- Overview statistics (total students, courses, attendance records)
- Recent students list
- Low attendance alerts (< 75%)
- Quick action buttons

### Student Management
- Add, edit, delete students
- View all students with search functionality
- Search by name, email, enrollment number, or course
- Individual student detail pages
- Course assignment to students
- Attendance percentage calculation

### Course Management
- Add, edit, delete courses
- View all courses
- Track enrolled students per course
- Unique course code validation

### Attendance Tracking
- Mark attendance (Present/Absent/Late)
- Filter by student, course, or date
- View attendance history
- Prevent duplicate entries
- Add remarks for each record

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python Flask 3.0 |
| Database | SQLite with SQLAlchemy ORM |
| Frontend | HTML5, CSS3, Bootstrap 5.3 |
| Templates | Jinja2 |
| Forms | Flask-WTF |
| Validation | WTForms validators |

## 📁 Project Structure

```
student-management-system/
├── app.py                      # Main application (Models + Controller)
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── PRD.md                      # Product Requirements Document
├── README.md                   # This file
├── static/
│   └── css/
│       └── style.css          # Custom styles
└── templates/
    ├── base.html              # Base layout template
    ├── dashboard.html         # Dashboard page
    ├── error.html             # Error pages (404, 500)
    ├── students/
    │   ├── list.html          # Student listing
    │   ├── form.html          # Add/Edit student form
    │   └── detail.html        # Student detail view
    ├── courses/
    │   ├── list.html          # Course listing
    │   └── form.html          # Add/Edit course form
    └── attendance/
        ├── list.html          # Attendance records
        └── mark.html          # Mark attendance form
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone or navigate to the project directory:**
   ```bash
   cd student-management-system
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Access the application:**
   Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## 📊 Database

The application uses SQLite database (`student_management.db`) which is automatically created on first run. Sample data is seeded automatically including:
- 5 sample students
- 5 sample courses
- Course assignments
- Sample attendance records

To reset the database, simply delete the `student_management.db` file and restart the application.

## 🔐 Authentication

**Note:** This is a simplified system without user authentication. In a production environment, you should add:
- User login/logout functionality
- Role-based access control
- Password hashing
- Session management

## 📝 MVC Architecture Explanation

This project follows the Model-View-Controller (MVC) pattern:

### Model (app.py - Lines 45-115)
- **Student**: Represents students table with relationships
- **Course**: Represents courses table
- **Attendance**: Represents attendance records
- **student_courses**: Association table for many-to-many relationship

### View (templates/)
- Jinja2 templates render HTML
- Extends `base.html` for consistent layout
- Uses Bootstrap for responsive design
- Displays flash messages for user feedback

### Controller (app.py - Routes)
- Handles HTTP requests
- Processes form submissions
- Interacts with models (database)
- Renders appropriate views
- Manages redirects and flash messages

## 🧪 Manual Test Checklist

### Dashboard
- [ ] Verify total counts are accurate
- [ ] Check recent students display correctly
- [ ] Confirm low attendance students are highlighted
- [ ] Test quick action buttons navigate correctly

### Student Management
- [ ] Create new student with all fields
- [ ] Verify unique enrollment number validation
- [ ] Verify unique email validation
- [ ] Edit existing student
- [ ] Delete student with confirmation
- [ ] Search by name, email, enrollment number
- [ ] Filter students by course
- [ ] View student details
- [ ] Assign course to student
- [ ] Remove course from student
- [ ] Verify duplicate course assignment prevention

### Course Management
- [ ] Create new course
- [ ] Verify unique course code validation
- [ ] Edit existing course
- [ ] Delete course with confirmation
- [ ] View student count per course

### Attendance Tracking
- [ ] Mark attendance for a student
- [ ] Verify required fields validation
- [ ] Test all status options (Present/Absent/Late)
- [ ] Add remarks
- [ ] Filter by student
- [ ] Filter by course
- [ ] Filter by date
- [ ] Verify duplicate prevention
- [ ] Check attendance percentage calculation
- [ ] Verify attendance history on student detail page

### General
- [ ] Test responsive design on mobile
- [ ] Verify flash messages appear correctly
- [ ] Test 404 error handling
- [ ] Confirm delete confirmations work
- [ ] Check empty states display properly

## 🔮 Future Enhancements

1. **User Authentication**
   - Login/logout system
   - Admin and teacher roles
   - Password reset functionality

2. **Advanced Features**
   - Bulk student import via CSV
   - Export reports to PDF/Excel
   - Email notifications for low attendance
   - Semester/term management
   - Grade tracking

3. **UI Improvements**
   - Dark mode toggle
   - Advanced charts and analytics
   - Calendar view for attendance
   - Mobile app version

4. **Technical Improvements**
   - PostgreSQL/MySQL support
   - REST API endpoints
   - Unit and integration tests
   - Docker containerization
   - CI/CD pipeline

## 📄 License

This project is created for educational purposes. Feel free to use and modify as needed.

## 👥 Support

For issues or questions:
1. Check the PRD.md for detailed requirements
2. Review the code comments in app.py
3. Ensure all dependencies are installed correctly

---

**Happy Managing! 🎓**
