-- SQL File: Teacher Profile Information for Tuition System
-- Database: tuition_system
-- Generated: 2026-05-05
-- This file contains all teacher data currently in your MySQL database

USE tuition_system;

-- =============================================
-- INSTRUCTION: How to import this SQL file
-- =============================================
-- Method 1: Using MySQL Command Line
-- mysql -u root -p tuition_system < teacher_profiles_import.sql
--
-- Method 2: Using phpMyAdmin (XAMPP)
-- 1. Open phpMyAdmin (http://localhost/phpmyadmin)
-- 2. Select 'tuition_system' database
-- 3. Go to 'Import' tab
-- 4. Choose this file and click 'Go'
--
-- Method 3: Using MySQL Workbench
-- 1. Connect to your MySQL instance
-- 2. Open this SQL file
-- 3. Execute the entire script
-- =============================================

-- =============================================
-- STEP 1: Clear existing teacher data (Optional)
-- Uncomment if you want to re-import fresh data
-- =============================================
-- DELETE FROM teacher_profiles;
-- DELETE FROM users WHERE role = 'teacher';

-- =============================================
-- STEP 2: Insert Teacher Users
-- Password for all teachers: password123
-- =============================================
INSERT INTO users (id, name, email, password_hash, role, is_active, is_approved, profile_picture, created_at) VALUES
(29, 'Dr. Ahmed Hassan', 'ahmed@tutor.com', 'pbkdf2:sha256:600000$wxyIOOb4HB27jnh1$48b1a21c5c74b0b2de32cd132b33f468e943b0d27b614648aa17d2eb6beb027b', 'teacher', 1, 1, '/static/Assets/Image/DemoTeacher1.png', NOW()),
(30, 'Sarah Rahman', 'sarah@tutor.com', 'pbkdf2:sha256:600000$wxyIOOb4HB27jnh1$48b1a21c5c74b0b2de32cd132b33f468e943b0d27b614648aa17d2eb6beb027b', 'teacher', 1, 1, '/static/Assets/Image/DemoTeacher2.png', NOW()),
(31, 'Mohammad Khan', 'khan@tutor.com', 'pbkdf2:sha256:600000$wxyIOOb4HB27jnh1$48b1a21c5c74b0b2de32cd132b33f468e943b0d27b614648aa17d2eb6beb027b', 'teacher', 1, 1, '/static/Assets/Image/DemoTeacher3.png', NOW()),
(32, 'Fatima Begum', 'fatima@tutor.com', 'pbkdf2:sha256:600000$wxyIOOb4HB27jnh1$48b1a21c5c74b0b2de32cd132b33f468e943b0d27b614648aa17d2eb6beb027b', 'teacher', 1, 1, '/static/Assets/Image/DemoTeacher4.png', NOW()),
(33, 'Abu Bakar', 'abubakar@tutor.com', 'pbkdf2:sha256:600000$wxyIOOb4HB27jnh1$48b1a21c5c74b0b2de32cd132b33f468e943b0d27b614648aa17d2eb6beb027b', 'teacher', 1, 1, '/static/Assets/Image/DemoTeacher5.png', NOW()),
(34, 'Lisa Ahmed', 'lisa@tutor.com', 'pbkdf2:sha256:600000$wxyIOOb4HB27jnh1$48b1a21c5c74b0b2de32cd132b33f468e943b0d27b614648aa17d2eb6beb027b', 'teacher', 1, 1, '/static/Assets/Image/DemoTeacher1.png', NOW()),
(35, 'Karim Chowdhury', 'karim@tutor.com', 'pbkdf2:sha256:600000$wxyIOOb4HB27jnh1$48b1a21c5c74b0b2de32cd132b33f468e943b0d27b614648aa17d2eb6beb027b', 'teacher', 1, 1, '/static/Assets/Image/DemoTeacher2.png', NOW()),
(36, 'Fatima Rahman', 'fatima2@tutor.com', 'pbkdf2:sha256:600000$wxyIOOb4HB27jnh1$48b1a21c5c74b0b2de32cd132b33f468e943b0d27b614648aa17d2eb6beb027b', 'teacher', 1, 1, '/static/Assets/Image/DemoTeacher3.png', NOW()),
(37, 'Sarah Akter', 'sarah2@tutor.com', 'pbkdf2:sha256:600000$wxyIOOb4HB27jnh1$48b1a21c5c74b0b2de32cd132b33f468e943b0d27b614648aa17d2eb6beb027b', 'teacher', 1, 1, '/static/Assets/Image/DemoTeacher5.png', NOW());

-- =============================================
-- STEP 3: Insert Teacher Profiles
-- =============================================
INSERT INTO teacher_profiles (user_id, university, department, degree, graduation_year, subject, experience, fee, location, bio, availability, is_complete, created_at) VALUES
(29, 'University of Dhaka', 'Department of Mathematics', 'BSc', 2014, 'Mathematics', 10, 5000, 'Dhanmondi, Dhaka', 'PhD in Mathematics with 10 years of teaching experience in SSC, HSC and University level.', 'Available', 1, NOW()),
(30, 'University of Dhaka', 'Department of English', 'BSc', 2017, 'English', 7, 4000, 'Gulshan, Dhaka', 'Native English speaker with expertise in grammar and literature.', 'Available', 1, NOW()),
(31, 'University of Dhaka', 'Department of Physics', 'BSc', 2016, 'Physics', 8, 5500, 'Mirpur, Dhaka', 'Experienced physics teacher for SSC and HSC students.', 'Available', 1, NOW()),
(32, 'University of Dhaka', 'Department of Chemistry', 'BSc', 2018, 'Chemistry', 6, 4500, 'Uttara, Dhaka', 'Chemistry specialist with practical lab experience.', 'Available', 1, NOW()),
(33, 'University of Dhaka', 'Department of Biology', 'BSc', 2015, 'Biology', 9, 4800, 'Banani, Dhaka', 'Medical graduate teaching biology for HSC and MBBS preparation.', 'Available', 1, NOW()),
(34, 'University of Dhaka', 'Department of Education', 'BSc', 2019, 'Class 1-5', 5, 3000, 'Baridhara, Dhaka', 'Patient teacher specialized in primary education.', 'Available', 1, NOW()),
(35, 'University of Dhaka', 'Department of ICT', 'BSc', 2018, 'ICT', 6, 4200, 'Mohammadpur, Dhaka', 'Expert in computer basics and programming for students.', 'Available', 1, NOW()),
(36, 'University of Dhaka', 'Department of Biology', 'BSc', 2017, 'Biology', 8, 1600, 'Dhanmondi, Dhaka', 'Specialized in HSC biology with practical approach.', 'Available', 1, NOW()),
(37, 'University of Dhaka', 'Department of English', 'BSc', 2019, 'English', 5, 1400, 'Gulshan, Dhaka', 'IELTS specialist with modern teaching methods.', 'Available', 1, NOW());

-- =============================================
-- STEP 4: Verification Queries
-- =============================================
SELECT 'Total Teachers in users table:' as Message, COUNT(*) as Count FROM users WHERE role = 'teacher'
UNION ALL
SELECT 'Total Profiles in teacher_profiles table:', COUNT(*) FROM teacher_profiles
UNION ALL
SELECT 'Teachers with Complete Profiles:', COUNT(*) FROM users u JOIN teacher_profiles tp ON u.id = tp.user_id WHERE u.role = 'teacher' AND tp.is_complete = 1;

-- =============================================
-- STEP 5: View All Teachers
-- =============================================
SELECT 
    u.id,
    u.name,
    u.email,
    tp.subject,
    tp.experience,
    tp.fee,
    tp.location,
    tp.availability
FROM users u
JOIN teacher_profiles tp ON u.id = tp.user_id
WHERE u.role = 'teacher'
ORDER BY u.id;

-- =============================================
-- END OF SQL FILE
-- =============================================
