"""
Database seeding script for Tuition System.
Run with: python seed.py
Reset with: python seed.py --reset
"""
import sys
import argparse
from firebase_db import FirebaseUser, FirebaseTeacherProfile

def seed_database(reset=False):
    print("=" * 50)
    print("Tuition System - Database Seeding")
    print("=" * 50)
    
    # Check if data already exists
    admin = FirebaseUser.get_by_email('admin@tuition.com')
    teacher_count = FirebaseUser.count(role='teacher')
    student_count = FirebaseUser.count(role='student')
    
    if reset:
        print("\n⚠️  Reset flag detected - clearing existing data...")
        # Note: Firebase doesn't have a simple "clear all" - would need to delete each document
        print("Reset functionality requires manual cleanup in Firebase Console.")
        print("Proceeding with fresh seed (will skip existing records)...")
    
    # Create Admin
    if not admin:
        FirebaseUser.create(
            name='Admin',
            email='admin@tuition.com',
            password='admin123',
            role='admin',
            is_active=True,
            is_approved=True
        )
        print("✓ Admin account created: admin@tuition.com / admin123")
    else:
        print("✓ Admin account already exists")
    
    # Create Sample Teachers
    if teacher_count == 0:
        sample_teachers = [
            {
                'name': 'Dr. Ahmed Hassan',
                'email': 'ahmed@tutor.com',
                'subject': 'Mathematics',
                'experience': 10,
                'fee': 5000,
                'location': 'Dhanmondi, Dhaka',
                'bio': 'PhD in Mathematics with 10 years of teaching experience in SSC, HSC and University level.',
                'university': 'University of Dhaka',
                'department': 'Department of Mathematics',
                'degree': 'PhD'
            },
            {
                'name': 'Sarah Rahman',
                'email': 'sarah@tutor.com',
                'subject': 'English',
                'experience': 7,
                'fee': 4000,
                'location': 'Gulshan, Dhaka',
                'bio': 'Native English speaker with expertise in grammar and literature.',
                'university': 'University of Dhaka',
                'department': 'Department of English',
                'degree': 'MA'
            },
            {
                'name': 'Mohammad Khan',
                'email': 'khan@tutor.com',
                'subject': 'Physics',
                'experience': 8,
                'fee': 5500,
                'location': 'Mirpur, Dhaka',
                'bio': 'Experienced physics teacher for SSC and HSC students.',
                'university': 'BUET',
                'department': 'Department of Physics',
                'degree': 'BSc'
            },
            {
                'name': 'Fatima Begum',
                'email': 'fatima@tutor.com',
                'subject': 'Chemistry',
                'experience': 6,
                'fee': 4500,
                'location': 'Uttara, Dhaka',
                'bio': 'Chemistry specialist with practical lab experience.',
                'university': 'University of Dhaka',
                'department': 'Department of Chemistry',
                'degree': 'MSc'
            },
            {
                'name': 'Abu Bakar',
                'email': 'abubakar@tutor.com',
                'subject': 'Biology',
                'experience': 9,
                'fee': 4800,
                'location': 'Banani, Dhaka',
                'bio': 'Medical graduate teaching biology for HSC and MBBS preparation.',
                'university': 'Sir Salimullah Medical College',
                'department': 'Medicine',
                'degree': 'MBBS'
            },
        ]
        
        for idx, t in enumerate(sample_teachers):
            user_id = FirebaseUser.create(
                name=t['name'],
                email=t['email'],
                password='password123',
                role='teacher',
                is_active=True,
                is_approved=True,
                profile_picture=f"/static/Assets/Image/DemoTeacher{(idx % 5) + 1}.png"
            )
            
            profile_data = {
                'subject': t['subject'],
                'university': t['university'],
                'department': t['department'],
                'degree': t['degree'],
                'graduation_year': 2020,
                'experience': t['experience'],
                'fee': t['fee'],
                'location': t['location'],
                'bio': t['bio'],
                'availability': 'Available',
                'is_complete': True
            }
            FirebaseTeacherProfile.create(user_id, profile_data)
        
        print(f"✓ Created {len(sample_teachers)} sample teachers")
    else:
        print(f"✓ {teacher_count} teachers already exist")
    
    # Create Sample Students
    if student_count == 0:
        sample_students = [
            {'name': 'Rahim Miya', 'email': 'rahim@student.com', 'password': 'password123'},
            {'name': 'Karim Ahmed', 'email': 'karim@student.com', 'password': 'password123'},
        ]
        
        for s in sample_students:
            FirebaseUser.create(
                name=s['name'],
                email=s['email'],
                password=s['password'],
                role='student',
                is_active=True,
                is_approved=True
            )
        
        print(f"✓ Created {len(sample_students)} sample students")
    else:
        print(f"✓ {student_count} students already exist")
    
    print("\n" + "=" * 50)
    print("Seeding completed successfully!")
    print("=" * 50)
    print("\nTest Credentials:")
    print("  Admin:  admin@tuition.com / admin123")
    print("  Student: rahim@student.com / password123")
    print("  Teacher: ahmed@tutor.com / password123")
    print("\nRun: python run.py")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Seed the database with sample data')
    parser.add_argument('--reset', action='store_true', help='Reset existing data before seeding')
    args = parser.parse_args()
    
    seed_database(reset=args.reset)
