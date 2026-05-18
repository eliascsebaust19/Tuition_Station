-- MySQL database schema for Elite Tuition Management System
CREATE DATABASE tuition_management;
USE tuition_management;

-- Languages table (if separate strings needed, but we use JSON or dual fields)
-- For simplicity, we'll store multilingual content in separate columns or use JSON.
-- Here we use a content table with language code.

CREATE TABLE courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_en VARCHAR(100),
    name_bn VARCHAR(100),
    description_en TEXT,
    description_bn TEXT,
    icon_class VARCHAR(50) DEFAULT 'fas fa-book-open'
);

CREATE TABLE faculty (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    subject_en VARCHAR(100),
    subject_bn VARCHAR(100),
    experience_years INT,
    photo_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE success_students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_en VARCHAR(100),
    name_bn VARCHAR(100),
    department_en VARCHAR(100),
    department_bn VARCHAR(100),
    class_en VARCHAR(50),
    class_bn VARCHAR(50),
    subject_en VARCHAR(100),
    subject_bn VARCHAR(100),
    city_en VARCHAR(100),
    city_bn VARCHAR(100),
    rating DECIMAL(2,1),
    match_date DATE
);

CREATE TABLE teacher_achievements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    qualification_en VARCHAR(150),
    qualification_bn VARCHAR(150),
    subject_en VARCHAR(100),
    subject_bn VARCHAR(100),
    students_found INT,
    location_en VARCHAR(100),
    location_bn VARCHAR(100)
);

CREATE TABLE notices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title_en VARCHAR(200),
    title_bn VARCHAR(200),
    content_en TEXT,
    content_bn TEXT,
    pdf_url TEXT,
    publish_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE contact_submissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    message TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Example insert for courses
INSERT INTO courses (name_en, name_bn, description_en, description_bn) VALUES
('SSC', 'এসএসসি', 'Comprehensive SSC preparation', 'সম্পূর্ণ এসএসসি প্রস্তুতি'),
('HSC', 'এইচএসসি', 'Expert HSC guidance', 'বিশেষজ্ঞ এইচএসসি নির্দেশনা'),
('Admission', 'ভর্তি প্রস্তুতি', 'University admission prep', 'বিশ্ববিদ্যালয় ভর্তি প্রস্তুতি'),
('Olympiad', 'অলিম্পিয়াড', 'Math & Science Olympiad', 'গণিত ও বিজ্ঞান অলিম্পিয়াড'),
('Competitive Exams', 'প্রতিযোগিতামূলক পরীক্ষা', 'BCS, Bank & more', 'বিসিএস, ব্যাংক ও অন্যান্য');

-- Additional tables for users, roles, etc. as needed.