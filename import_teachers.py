import pymysql
from werkzeug.security import generate_password_hash
from datetime import datetime

# Generate password hash
password_hash = generate_password_hash('password123')

# Connect to MySQL
conn = pymysql.connect(host='localhost', user='root', password='', database='tuition_system')
cursor = conn.cursor()

# Clear existing teacher data
print("Clearing existing teacher data...")
cursor.execute("DELETE FROM teacher_profiles")
cursor.execute("DELETE FROM users WHERE role = 'teacher'")

# Teacher data
teachers = [
    ('Dr. Ahmed Hassan', 'ahmed@tutor.com', '/static/Assets/Image/DemoTeacher1.png', 
     'Mathematics', 10, 5000, 'Dhanmondi, Dhaka', 'PhD in Mathematics with 10 years of teaching experience in SSC, HSC and University level.'),
    ('Sarah Rahman', 'sarah@tutor.com', '/static/Assets/Image/DemoTeacher2.png',
     'English', 7, 4000, 'Gulshan, Dhaka', 'Native English speaker with expertise in grammar and literature.'),
    ('Mohammad Khan', 'khan@tutor.com', '/static/Assets/Image/DemoTeacher3.png',
     'Physics', 8, 5500, 'Mirpur, Dhaka', 'Experienced physics teacher for SSC and HSC students.'),
    ('Fatima Begum', 'fatima@tutor.com', '/static/Assets/Image/DemoTeacher4.png',
     'Chemistry', 6, 4500, 'Uttara, Dhaka', 'Chemistry specialist with practical lab experience.'),
    ('Abu Bakar', 'abubakar@tutor.com', '/static/Assets/Image/DemoTeacher5.png',
     'Biology', 9, 4800, 'Banani, Dhaka', 'Medical graduate teaching biology for HSC and MBBS preparation.'),
    ('Lisa Ahmed', 'lisa@tutor.com', '/static/Assets/Image/DemoTeacher1.png',
     'Class 1-5', 5, 3000, 'Baridhara, Dhaka', 'Patient teacher specialized in primary education.'),
    ('Karim Chowdhury', 'karim@tutor.com', '/static/Assets/Image/DemoTeacher2.png',
     'ICT', 6, 4200, 'Mohammadpur, Dhaka', 'Expert in computer basics and programming for students.'),
    ('Fatima Rahman', 'fatima2@tutor.com', '/static/Assets/Image/DemoTeacher3.png',
     'Biology', 8, 1600, 'Dhanmondi, Dhaka', 'Specialized in HSC biology with practical approach.'),
    ('Sarah Akter', 'sarah2@tutor.com', '/static/Assets/Image/DemoTeacher5.png',
     'English', 5, 1400, 'Gulshan, Dhaka', 'IELTS specialist with modern teaching methods.'),
]

print("Inserting teacher users and profiles...")

for idx, (name, email, pic, subject, exp, fee, location, bio) in enumerate(teachers):
    # Insert user
    cursor.execute(
        """INSERT INTO users (name, email, password_hash, role, is_active, is_approved, profile_picture, created_at) 
           VALUES (%s, %s, %s, 'teacher', 1, 1, %s, NOW())""",
        (name, email, password_hash, pic)
    )
    
    # Get the user_id
    user_id = cursor.lastrowid
    
    # Insert teacher profile
    cursor.execute(
        """INSERT INTO teacher_profiles (user_id, university, department, degree, graduation_year, 
           subject, experience, fee, location, bio, availability, is_complete, created_at) 
           VALUES (%s, 'University of Dhaka', %s, 'BSc', 2015, %s, %s, %s, %s, %s, 'Available', 1, NOW())""",
        (user_id, f'Department of {subject}', subject, exp, fee, location, bio)
    )
    
    print(f"Inserted: {name} - {subject}")

conn.commit()

# Verify
cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'teacher'")
teacher_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM teacher_profiles")
profile_count = cursor.fetchone()[0]

print("\nImport completed!")
print(f"Teachers in users table: {teacher_count}")
print(f"Profiles in teacher_profiles table: {profile_count}")

# Show all teachers
print("\nTeacher List:")
cursor.execute("""
    SELECT u.id, u.name, u.email, tp.subject, tp.experience, tp.fee, tp.location 
    FROM users u 
    JOIN teacher_profiles tp ON u.id = tp.user_id 
    WHERE u.role = 'teacher'
    ORDER BY u.id
""")

for row in cursor.fetchall():
    print(f"ID: {row[0]}, Name: {row[1]}, Subject: {row[3]}, Fee: {row[5]}, Exp: {row[4]} years")

cursor.close()
conn.close()
