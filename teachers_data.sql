-- SQL file to import teacher profile information into tuition_system database
-- Generated for MySQL/XAMPP

USE tuition_system;

-- Clear existing data (optional, comment out if you want to keep existing data)
-- DELETE FROM teacher_profiles;
-- DELETE FROM users WHERE role = 'teacher';

-- Insert Teacher Users (Password: password123 - hashed)
INSERT INTO users (name, email, password_hash, role, is_active, is_approved, profile_picture, created_at) VALUES
('Dr. Ahmed Hassan', 'ahmed@tutor.com', '$2b$12$LQv...hashed_password...', 'teacher', 1, 1, '/static/Assets/Image/DemoTeacher1.png', NOW()),
('Sarah Rahman', 'sarah@tutor.com', '$2b$12$LQv...hashed_password...', 'teacher', 1, 1, '/static/Assets/Image/DemoTeacher2.png', NOW()),
('Mohammad Khan', 'khan@tutor.com', '$2b$12$LQv...hashed_password...', 'teacher', 1, 1, '/static/Assets/Image/DemoTeacher3.png', NOW()),
('Fatima Begum', 'fatima@tutor.com', '$2b$12$LQv...hashed_password...', 'teacher', 1, 1, '/static/Assets/Image/DemoTeacher4.png', NOW()),
('Abu Bakar', 'abubakar@tutor.com', '$2b$12$LQv...hashed_password...', 'teacher', 1, 1, '/static/Assets/Image/DemoTeacher5.png', NOW()),
('Lisa Ahmed', 'lisa@tutor.com', '$2b$12$LQv...hashed_password...', 'teacher', 1, 1, '/static/Assets/Image/DemoTeacher1.png', NOW()),
('Karim Chowdhury', 'karim@tutor.com', '$2b$12$LQv...hashed_password...', 'teacher', 1, 1, '/static/Assets/Image/DemoTeacher2.png', NOW()),
('Fatima Rahman', 'fatima2@tutor.com', '$2b$12$LQv...hashed_password...', 'teacher', 1, 1, '/static/Assets/Image/DemoTeacher3.png', NOW()),
('Sarah Akter', 'sarah2@tutor.com', '$2b$12$LQv...hashed_password...', 'teacher', 1, 1, '/static/Assets/Image/DemoTeacher5.png', NOW());

-- Insert Teacher Profiles
INSERT INTO teacher_profiles (user_id, university, department, degree, graduation_year, masters_university, masters_department, masters_year, subject, experience, fee, location, bio, availability, is_complete, cv, created_at) VALUES
(1, 'University of Dhaka', 'Department of Mathematics', 'BSc', 2014, NULL, NULL, NULL, 'Mathematics', 10, 5000, 'Dhanmondi, Dhaka', 'PhD in Mathematics with 10 years of teaching experience in SSC, HSC and University level.', 'Available', 1, NULL, NOW()),
(2, 'University of Dhaka', 'Department of English', 'BSc', 2017, NULL, NULL, NULL, 'English', 7, 4000, 'Gulshan, Dhaka', 'Native English speaker with expertise in grammar and literature.', 'Available', 1, NULL, NOW()),
(3, 'University of Dhaka', 'Department of Physics', 'BSc', 2016, NULL, NULL, NULL, 'Physics', 8, 5500, 'Mirpur, Dhaka', 'Experienced physics teacher for SSC and HSC students.', 'Available', 1, NULL, NOW()),
(4, 'University of Dhaka', 'Department of Chemistry', 'BSc', 2018, NULL, NULL, NULL, 'Chemistry', 6, 4500, 'Uttara, Dhaka', 'Chemistry specialist with practical lab experience.', 'Available', 1, NULL, NOW()),
(5, 'University of Dhaka', 'Department of Biology', 'BSc', 2015, NULL, NULL, NULL, 'Biology', 9, 4800, 'Banani, Dhaka', 'Medical graduate teaching biology for HSC and MBBS preparation.', 'Available', 1, NULL, NOW()),
(6, 'University of Dhaka', 'Department of Education', 'BSc', 2019, NULL, NULL, NULL, 'Class 1-5', 5, 3000, 'Baridhara, Dhaka', 'Patient teacher specialized in primary education.', 'Available', 1, NULL, NOW()),
(7, 'University of Dhaka', 'Department of ICT', 'BSc', 2018, NULL, NULL, NULL, 'ICT', 6, 4200, 'Mohammadpur, Dhaka', 'Expert in computer basics and programming for students.', 'Available', 1, NULL, NOW()),
(8, 'University of Dhaka', 'Department of Biology', 'BSc', 2017, NULL, NULL, NULL, 'Biology', 8, 1600, 'Dhanmondi, Dhaka', 'Specialized in HSC biology with practical approach.', 'Available', 1, NULL, NOW()),
(9, 'University of Dhaka', 'Department of English', 'BSc', 2019, NULL, NULL, NULL, 'English', 5, 1400, 'Gulshan, Dhaka', 'IELTS specialist with modern teaching methods.', 'Available', 1, NULL, NOW());

-- Verify the data
SELECT 'Teachers inserted:' as Message, COUNT(*) as Count FROM users WHERE role = 'teacher';
SELECT 'Profiles inserted:' as Message, COUNT(*) as Count FROM teacher_profiles;
