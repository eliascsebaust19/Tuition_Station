-- Add teaching_mode column
IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('teacher_profiles') AND name = 'teaching_mode')
    ALTER TABLE teacher_profiles ADD teaching_mode VARCHAR(20) DEFAULT 'both' NOT NULL;
GO
PRINT 'Added teaching_mode column';

-- Copy data from online_available
IF EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID('teacher_profiles') AND name = 'online_available')
BEGIN
    UPDATE teacher_profiles SET teaching_mode = CASE WHEN online_available = 1 THEN 'both' ELSE 'offline' END;
    PRINT 'Migrated online_available data';
END
GO

-- Fill any nulls
UPDATE teacher_profiles SET teaching_mode = 'both' WHERE teaching_mode IS NULL;
GO
PRINT 'Migration complete';
GO
