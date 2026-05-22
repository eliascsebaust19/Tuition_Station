from werkzeug.security import generate_password_hash
from datetime import datetime

# Generate hashed password
password = 'password123'
hashed = generate_password_hash(password)

print("-- SQL file to import teacher profile information into tuition_system database")
print("-- Generated for MySQL/XAMPP")
print()
print("USE tuition_system;")
print()
print("-- Clear existing teacher data (optional)")
print("-- DELETE FROM teacher_profiles;")
print("-- DELETE FROM users WHERE role = 'teacher';")
print()
print("-- Insert Teacher Users (Password: password123)")
print("INSERT INTO users (name, email, password_hash, role, is_active, is_approved, profile_picture, created_at) VALUES")

teachers = [
    ('Dr. Ahmed Hassan', 'ahmed@tutor.com', '/static/Assets/Image/DemoTeacher1.png', 'Mathematics', 10, 5000, 'Dhanmondi, Dhaka', 'PhD in Mathematics with 10 years of teaching experience in SSC, HSC and University level.'),
    ('Sarah Rahman', 'sarah@tutor.com', '/static/Assets/Image/DemoTeacher2.png', 'English', 7, 4000, 'Gulshan, Dhaka', 'Native English speaker with expertise in grammar and literature.'),
    ('Mohammad Khan', 'khan@tutor.com', '/static/Assets/Image/DemoTeacher3.png', 'Physics', 8, 5500, 'Mirpur, Dhaka', 'Experienced physics teacher for SSC and HSC students.'),
    ('Fatima Begum', 'fatima@tutor.com', '/static/Assets/Image/DemoTeacher4.png', 'Chemistry', 6, 4500, 'Uttara, Dhaka', 'Chemistry specialist with practical lab experience.'),
    ('Abu Bakar', 'abubakar@tutor.com', '/static/Assets/Image/DemoTeacher5.png', 'Biology', 9, 4800, 'Banani, Dhaka', 'Medical graduate teaching biology for HSC and MBBS preparation.'),
    ('Lisa Ahmed', 'lisa@tutor.com', '/static/Assets/Image/DemoTeacher1.png', 'Class 1-5', 5, 3000, 'Baridhara, Dhaka', 'Patient teacher specialized in primary education.'),
    ('Karim Chowdhury', 'karim@tutor.com', '/static/Assets/Image/DemoTeacher2.png', 'ICT', 6, 4200, 'Mohammadpur, Dhaka', 'Expert in computer basics and programming for students.'),
    ('Fatima Rahman', 'fatima2@tutor.com', '/static/Assets/Image/DemoTeacher3.png', 'Biology', 8, 1600, 'Dhanmondi, Dhaka', 'Specialized in HSC biology with practical approach.'),
    ('Sarah Akter', 'sarah2@tutor.com', '/static/Assets/Image/DemoTeacher5.png', 'English', 5, 1400, 'Gulshan, Dhaka', 'IELTS specialist with modern teaching methods.'),
]

for i, (name, email, pic, subject, exp, fee, location, bio) in enumerate(teachers):
    comma = ',' if i < len(teachers) - 1 else ';'
    print(f"('{name}', '{email}', '{hashed}', 'teacher', 1, 1, '{pic}', NOW()){comma}")

print()
print("-- Insert Teacher Profiles")
print("INSERT INTO teacher_profiles (user_id, university, department, degree, graduation_year, subject, experience, fee, location, bio, availability, is_complete, created_at) VALUES")

for i, (name, email, pic, subject, exp, fee, location, bio) in enumerate(teachers):
    comma = ',' if i < len(teachers) - 1 else ';'
    user_id = i + 1  # Assuming user IDs start from 1
    print(f"({user_id}, 'University of Dhaka', 'Department of {subject}', 'BSc', 2015, '{subject}', {exp}, {fee}, '{location}', '{bio}', 'Available', 1, NOW()){comma}")

print()
print("-- Verify the data")
print("SELECT 'Teachers inserted:' as Message, COUNT(*) as Count FROM users WHERE role = 'teacher';")
print("SELECT 'Profiles inserted:' as Message, COUNT(*) as Count FROM teacher_profiles;")
