-- Migration: Add new teacher profile fields
-- Run this if teacher_profiles table already exists

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('teacher_profiles') AND name = 'hourly_fee')
    ALTER TABLE teacher_profiles ADD hourly_fee INT NULL;

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('teacher_profiles') AND name = 'qualification')
    ALTER TABLE teacher_profiles ADD qualification TEXT NULL;

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('teacher_profiles') AND name = 'subjects_expert_in')
    ALTER TABLE teacher_profiles ADD subjects_expert_in TEXT NULL;

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('teacher_profiles') AND name = 'class_level')
    ALTER TABLE teacher_profiles ADD class_level VARCHAR(100) NULL;

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('teacher_profiles') AND name = 'teaching_areas')
    ALTER TABLE teacher_profiles ADD teaching_areas TEXT NULL;

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('teacher_profiles') AND name = 'online_available')
    ALTER TABLE teacher_profiles ADD online_available BIT DEFAULT 1;

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('teacher_profiles') AND name = 'demo_class_available')
    ALTER TABLE teacher_profiles ADD demo_class_available BIT DEFAULT 0;

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('teacher_profiles') AND name = 'total_students_taught')
    ALTER TABLE teacher_profiles ADD total_students_taught INT DEFAULT 0;

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('teacher_profiles') AND name = 'success_percentage')
    ALTER TABLE teacher_profiles ADD success_percentage INT NULL;

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('teacher_profiles') AND name = 'languages')
    ALTER TABLE teacher_profiles ADD languages VARCHAR(200) NULL;

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('teacher_profiles') AND name = 'teaching_style')
    ALTER TABLE teacher_profiles ADD teaching_style TEXT NULL;

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('teacher_profiles') AND name = 'availability_schedule')
    ALTER TABLE teacher_profiles ADD availability_schedule TEXT NULL;

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('teacher_profiles') AND name = 'social_links')
    ALTER TABLE teacher_profiles ADD social_links TEXT NULL;

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('teacher_profiles') AND name = 'intro_video_url')
    ALTER TABLE teacher_profiles ADD intro_video_url VARCHAR(500) NULL;

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('teacher_profiles') AND name = 'notes_resources')
    ALTER TABLE teacher_profiles ADD notes_resources TEXT NULL;

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('teacher_profiles') AND name = 'key_strengths')
    ALTER TABLE teacher_profiles ADD key_strengths TEXT NULL;

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('teacher_profiles') AND name = 'why_students_notice')
    ALTER TABLE teacher_profiles ADD why_students_notice TEXT NULL;

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('teacher_profiles') AND name = 'tuition_experience')
    ALTER TABLE teacher_profiles ADD tuition_experience TEXT NULL;

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('teacher_profiles') AND name = 'reasons_to_hire')
    ALTER TABLE teacher_profiles ADD reasons_to_hire TEXT NULL;

IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('teacher_profiles') AND name = 'preface')
    ALTER TABLE teacher_profiles ADD preface TEXT NULL;

PRINT 'Migration completed: New columns added to teacher_profiles table';
