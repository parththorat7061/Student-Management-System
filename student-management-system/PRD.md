# Student Management System - Product Requirements Document (PRD)

## 1. Problem Statement

College administrators and academic coordinators need a simple, centralized system to manage student records, course assignments, and attendance tracking. Currently, this data may be scattered across spreadsheets or paper records, making it difficult to:
- Quickly access student information
- Track which courses each student is enrolled in
- Monitor attendance patterns and identify at-risk students
- Generate reports on overall enrollment and attendance statistics

## 2. Objectives

- Build a web-based CRUD application for managing students, courses, and attendance
- Provide a clean, intuitive dashboard for quick overview of key metrics
- Enable easy assignment of courses to students with validation
- Track daily attendance with multiple status options
- Display attendance percentages to identify students needing intervention
- Create a maintainable, well-structured codebase following MVC architecture

## 3. User Roles

| Role | Description |
|------|-------------|
| Admin/User | Single user role with full access to all features (no authentication required for simplicity) |

## 4. Functional Requirements

### 4.1 Dashboard
- Display total count of students, courses, and attendance records
- Show list of recently added students (last 5)
- Highlight students with attendance below 75%
- Provide quick action buttons for common tasks

### 4.2 Student Management
- Create new student with all required fields
- Edit existing student information
- Delete student with confirmation
- View all students in a searchable table
- View detailed student profile including assigned courses and attendance history
- Search by name, email, enrollment number, or course

### 4.3 Course Management
- Create new course with code, name, description, and credits
- Edit existing course details
- Delete course with confirmation
- View all courses in a table format

### 4.4 Course Assignment
- Assign one or more courses to a student
- Prevent duplicate assignments
- Remove course assignments
- Display assigned courses on student detail page

### 4.5 Attendance Tracking
- Mark attendance for individual students per course
- Support three statuses: Present, Absent, Late
- Add optional remarks for each attendance record
- Filter attendance records by student, course, or date
- Calculate and display attendance percentage per student
- Show complete attendance history on student detail page

## 5. Non-Functional Requirements

- **Performance**: Pages should load within 2 seconds for typical data volumes
- **Usability**: Clean Bootstrap-based UI, responsive design, intuitive navigation
- **Maintainability**: MVC architecture with clear separation of concerns
- **Data Integrity**: Proper validation, unique constraints, relationship integrity
- **Scalability**: Design should support growth to hundreds of students and courses
- **Browser Compatibility**: Works on modern browsers (Chrome, Firefox, Safari, Edge)

## 6. Database Schema

### Tables

#### students
```
id (INTEGER, PRIMARY KEY)
enrollment_number (VARCHAR, UNIQUE, NOT NULL)
first_name (VARCHAR, NOT NULL)
last_name (VARCHAR, NOT NULL)
email (VARCHAR, UNIQUE, NOT NULL)
phone (VARCHAR)
date_of_birth (DATE)
gender (VARCHAR)
address (TEXT)
created_at (DATETIME)
updated_at (DATETIME)
```

#### courses
```
id (INTEGER, PRIMARY KEY)
course_code (VARCHAR, UNIQUE, NOT NULL)
course_name (VARCHAR, NOT NULL)
description (TEXT)
credits (INTEGER)
created_at (DATETIME)
updated_at (DATETIME)
```

#### student_courses (Association Table)
```
student_id (INTEGER, FOREIGN KEY -> students.id)
course_id (INTEGER, FOREIGN KEY -> courses.id)
PRIMARY KEY (student_id, course_id)
```

#### attendance
```
id (INTEGER, PRIMARY KEY)
student_id (INTEGER, FOREIGN KEY -> students.id, NOT NULL)
course_id (INTEGER, FOREIGN KEY -> courses.id, NOT NULL)
attendance_date (DATE, NOT NULL)
status (VARCHAR, NOT NULL) -- 'Present', 'Absent', 'Late'
remarks (TEXT)
created_at (DATETIME)
```

## 7. Route List

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Dashboard |
| GET | `/students` | List/search students |
| GET | `/students/add` | Add student form |
| POST | `/students/add` | Create student |
| GET | `/students/<id>` | Student details |
| GET | `/students/<id>/edit` | Edit student form |
| POST | `/students/<id>/edit` | Update student |
| POST | `/students/<id>/delete` | Delete student |
| POST | `/students/<id>/assign-course` | Assign course to student |
| POST | `/students/<id>/remove-course/<course_id>` | Remove course from student |
| GET | `/courses` | List courses |
| GET | `/courses/add` | Add course form |
| POST | `/courses/add` | Create course |
| GET | `/courses/<id>/edit` | Edit course form |
| POST | `/courses/<id>/edit` | Update course |
| POST | `/courses/<id>/delete` | Delete course |
| GET | `/attendance` | Attendance records with filters |
| GET | `/attendance/mark` | Mark attendance form |
| POST | `/attendance/mark` | Save attendance record |

## 8. MVC Mapping

### Model (app.py)
- `Student` class: ORM model for students table
- `Course` class: ORM model for courses table
- `Attendance` class: ORM model for attendance table
- `student_courses` association table for many-to-many relationship

### View (templates/)
- `base.html`: Base layout with navbar and flash messages
- `dashboard.html`: Dashboard with statistics and quick links
- `students/list.html`: Student listing with search
- `students/form.html`: Add/edit student form
- `students/detail.html`: Student detail view
- `courses/list.html`: Course listing
- `courses/form.html`: Add/edit course form
- `attendance/list.html`: Attendance records with filters
- `attendance/mark.html`: Mark attendance form

### Controller (app.py)
- Dashboard routes
- Student CRUD routes
- Course CRUD routes
- Course assignment routes
- Attendance CRUD and filter routes
- Search functionality

## 9. Acceptance Criteria

### Dashboard
- [ ] Shows correct counts for students, courses, and attendance records
- [ ] Displays up to 5 most recently added students
- [ ] Lists students with attendance below 75%
- [ ] Quick action buttons navigate to correct pages

### Student Management
- [ ] Can create student with all required fields
- [ ] Enrollment number and email must be unique
- [ ] Can edit existing student information
- [ ] Can delete student with confirmation
- [ ] Search works by name, email, enrollment number, and course
- [ ] Student detail page shows assigned courses and attendance history
- [ ] Attendance percentage is calculated correctly

### Course Management
- [ ] Can create course with all required fields
- [ ] Course code must be unique
- [ ] Can edit existing course
- [ ] Can delete course with confirmation

### Course Assignment
- [ ] Can assign course to student
- [ ] Cannot assign same course twice to same student
- [ ] Can remove course assignment
- [ ] Assigned courses appear on student detail page

### Attendance Tracking
- [ ] Can mark attendance with status (Present/Absent/Late)
- [ ] Requires student, course, date, and status
- [ ] Can add optional remarks
- [ ] Can filter by student, course, and date
- [ ] Attendance percentage updates correctly
- [ ] History shows on student detail page

### General
- [ ] All forms have proper validation
- [ ] Flash messages show for success/error actions
- [ ] Delete actions require confirmation
- [ ] Empty states display when no data exists
- [ ] UI is responsive and works on mobile devices
- [ ] Navigation works correctly across all pages
- [ ] Application runs without errors on first setup

---

**Status**: Ready for Implementation
**Version**: 1.0
**Date**: Current
