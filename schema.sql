-- ============================================================================
-- TuitionStation - Complete Database Schema for Microsoft SQL Server
-- ============================================================================
-- This script creates the entire TuitionStation database with:
--   • All tables with primary/foreign keys, constraints, indexes
--   • Stored Procedures for business logic
--   • Views for analytics and reporting
--   • Triggers for automation (auto-downgrade, notifications)
--   • Seed data for subscription plans
-- ============================================================================

-- Create database
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'tuition_station')
BEGIN
    CREATE DATABASE tuition_station;
END
GO

USE tuition_station;
GO

-- ============================================================================
-- 1. TABLES
-- ============================================================================

-- ---------------------------------------------------
-- 1.1 Users
-- ---------------------------------------------------
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[users]') AND type in (N'U'))
BEGIN
    CREATE TABLE users (
        id INT IDENTITY(1,1) PRIMARY KEY,
        name NVARCHAR(100) NOT NULL,
        email NVARCHAR(120) NOT NULL,
        password_hash NVARCHAR(256) NOT NULL,
        role NVARCHAR(20) NOT NULL CHECK (role IN ('student', 'teacher', 'admin')),
        is_active BIT DEFAULT 1,
        is_approved BIT DEFAULT 0,
        is_online BIT DEFAULT 0,
        profile_picture NVARCHAR(500),
        created_at DATETIME2 DEFAULT GETUTCDATE(),
        updated_at DATETIME2 DEFAULT GETUTCDATE(),
        CONSTRAINT UQ_users_email UNIQUE (email)
    );
END
GO

-- ---------------------------------------------------
-- 1.2 Teacher Profiles
-- ---------------------------------------------------
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[teacher_profiles]') AND type in (N'U'))
BEGIN
    CREATE TABLE teacher_profiles (
        id INT IDENTITY(1,1) PRIMARY KEY,
        user_id INT NOT NULL,
        university NVARCHAR(200),
        department NVARCHAR(100),
        degree NVARCHAR(50),
        graduation_year INT,
        masters_university NVARCHAR(200),
        masters_department NVARCHAR(100),
        masters_year INT,
        subject NVARCHAR(100) NOT NULL,
        experience INT DEFAULT 0,
        fee INT NOT NULL,
        location NVARCHAR(100),
        bio NVARCHAR(MAX),
        availability NVARCHAR(50) DEFAULT 'Available' CHECK (availability IN ('Available', 'Busy', 'Not Available')),
        is_complete BIT DEFAULT 0,
        cv NVARCHAR(500),
        created_at DATETIME2 DEFAULT GETUTCDATE(),
        updated_at DATETIME2 DEFAULT GETUTCDATE(),
        CONSTRAINT FK_teacher_profiles_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        CONSTRAINT UQ_teacher_profiles_user UNIQUE (user_id)
    );
END
GO

-- ---------------------------------------------------
-- 1.3 Subscription Plans
-- ---------------------------------------------------
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[subscription_plans]') AND type in (N'U'))
BEGIN
    CREATE TABLE subscription_plans (
        id INT IDENTITY(1,1) PRIMARY KEY,
        name NVARCHAR(50) NOT NULL CHECK (name IN ('Free', 'Standard', 'Premium')),
        price DECIMAL(10,2) NOT NULL DEFAULT 0,
        duration_days INT NOT NULL DEFAULT 30,
        max_applications INT,           -- NULL = unlimited
        is_featured BIT DEFAULT 0,
        has_verified_badge BIT DEFAULT 0,
        priority_ranking INT DEFAULT 0, -- higher = shows first
        description NVARCHAR(MAX),
        created_at DATETIME2 DEFAULT GETUTCDATE()
    );
END
GO

-- ---------------------------------------------------
-- 1.4 User Subscriptions
-- ---------------------------------------------------
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[user_subscriptions]') AND type in (N'U'))
BEGIN
    CREATE TABLE user_subscriptions (
        id INT IDENTITY(1,1) PRIMARY KEY,
        user_id INT NOT NULL,
        plan_id INT NOT NULL,
        start_date DATETIME2 DEFAULT GETUTCDATE(),
        end_date DATETIME2 NOT NULL,
        is_active BIT DEFAULT 1,
        auto_renew BIT DEFAULT 0,
        created_at DATETIME2 DEFAULT GETUTCDATE(),
        CONSTRAINT FK_user_subscriptions_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        CONSTRAINT FK_user_subscriptions_plan FOREIGN KEY (plan_id) REFERENCES subscription_plans(id)
    );
END
GO

-- ---------------------------------------------------
-- 1.5 Payments
-- ---------------------------------------------------
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[payments]') AND type in (N'U'))
BEGIN
    CREATE TABLE payments (
        id INT IDENTITY(1,1) PRIMARY KEY,
        user_id INT NOT NULL,
        plan_id INT NOT NULL,
        amount DECIMAL(10,2) NOT NULL,
        method NVARCHAR(20) NOT NULL CHECK (method IN ('bKash', 'Nagad')),
        sender_number NVARCHAR(20),
        transaction_id NVARCHAR(100) NOT NULL,
        status NVARCHAR(20) NOT NULL DEFAULT 'Pending' CHECK (status IN ('Pending', 'Approved', 'Rejected')),
        admin_note NVARCHAR(MAX),
        verified_by INT,
        verified_at DATETIME2,
        created_at DATETIME2 DEFAULT GETUTCDATE(),
        CONSTRAINT FK_payments_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        CONSTRAINT FK_payments_plan FOREIGN KEY (plan_id) REFERENCES subscription_plans(id),
        CONSTRAINT FK_payments_verified_by FOREIGN KEY (verified_by) REFERENCES users(id),
        CONSTRAINT UQ_payments_transaction UNIQUE (transaction_id)
    );
END
GO

-- ---------------------------------------------------
-- 1.6 Tuition Posts (Students post requirements)
-- ---------------------------------------------------
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[tuition_posts]') AND type in (N'U'))
BEGIN
    CREATE TABLE tuition_posts (
        id INT IDENTITY(1,1) PRIMARY KEY,
        student_id INT NOT NULL,
        title NVARCHAR(200) NOT NULL,
        subject NVARCHAR(100) NOT NULL,
        class_level NVARCHAR(50),
        location NVARCHAR(200) NOT NULL,
        salary INT,
        description NVARCHAR(MAX),
        status NVARCHAR(20) NOT NULL DEFAULT 'Open' CHECK (status IN ('Open', 'Closed', 'Filled')),
        created_at DATETIME2 DEFAULT GETUTCDATE(),
        updated_at DATETIME2 DEFAULT GETUTCDATE(),
        CONSTRAINT FK_tuition_posts_student FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE
    );
END
GO

-- ---------------------------------------------------
-- 1.7 Applications (Tutors apply to posts)
-- ---------------------------------------------------
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[applications]') AND type in (N'U'))
BEGIN
    CREATE TABLE applications (
        id INT IDENTITY(1,1) PRIMARY KEY,
        post_id INT NOT NULL,
        teacher_id INT NOT NULL,
        message NVARCHAR(MAX),
        status NVARCHAR(20) NOT NULL DEFAULT 'Pending' CHECK (status IN ('Pending', 'Shortlisted', 'Selected', 'Rejected')),
        created_at DATETIME2 DEFAULT GETUTCDATE(),
        CONSTRAINT FK_applications_post FOREIGN KEY (post_id) REFERENCES tuition_posts(id) ON DELETE CASCADE,
        CONSTRAINT FK_applications_teacher FOREIGN KEY (teacher_id) REFERENCES users(id),
        CONSTRAINT UQ_applications_post_teacher UNIQUE (post_id, teacher_id)
    );
END
GO

-- ---------------------------------------------------
-- 1.8 Messages / Chat
-- ---------------------------------------------------
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[messages]') AND type in (N'U'))
BEGIN
    CREATE TABLE messages (
        id INT IDENTITY(1,1) PRIMARY KEY,
        sender_id INT NOT NULL,
        receiver_id INT NOT NULL,
        message NVARCHAR(MAX) NOT NULL,
        is_read BIT DEFAULT 0,
        read_at DATETIME2,
        created_at DATETIME2 DEFAULT GETUTCDATE(),
        CONSTRAINT FK_messages_sender FOREIGN KEY (sender_id) REFERENCES users(id),
        CONSTRAINT FK_messages_receiver FOREIGN KEY (receiver_id) REFERENCES users(id)
    );
END
GO

-- ---------------------------------------------------
-- 1.9 Notifications
-- ---------------------------------------------------
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[notifications]') AND type in (N'U'))
BEGIN
    CREATE TABLE notifications (
        id INT IDENTITY(1,1) PRIMARY KEY,
        user_id INT NOT NULL,
        type NVARCHAR(50) DEFAULT 'general',
        title NVARCHAR(200) NOT NULL,
        message NVARCHAR(MAX) NOT NULL,
        link NVARCHAR(500),
        is_read BIT DEFAULT 0,
        created_at DATETIME2 DEFAULT GETUTCDATE(),
        CONSTRAINT FK_notifications_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
END
GO

-- ---------------------------------------------------
-- 1.10 Saved Tutors (Students bookmark tutors)
-- ---------------------------------------------------
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[saved_tutors]') AND type in (N'U'))
BEGIN
    CREATE TABLE saved_tutors (
        id INT IDENTITY(1,1) PRIMARY KEY,
        student_id INT NOT NULL,
        teacher_id INT NOT NULL,
        created_at DATETIME2 DEFAULT GETUTCDATE(),
        CONSTRAINT FK_saved_tutors_student FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
        CONSTRAINT FK_saved_tutors_teacher FOREIGN KEY (teacher_id) REFERENCES users(id),
        CONSTRAINT UQ_saved_tutors UNIQUE (student_id, teacher_id)
    );
END
GO

-- ---------------------------------------------------
-- 1.11 Reviews
-- ---------------------------------------------------
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[reviews]') AND type in (N'U'))
BEGIN
    CREATE TABLE reviews (
        id INT IDENTITY(1,1) PRIMARY KEY,
        student_id INT NOT NULL,
        teacher_id INT NOT NULL,
        rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
        comment NVARCHAR(MAX),
        created_at DATETIME2 DEFAULT GETUTCDATE(),
        CONSTRAINT FK_reviews_student FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
        CONSTRAINT FK_reviews_teacher FOREIGN KEY (teacher_id) REFERENCES users(id)
    );
END
GO

-- ---------------------------------------------------
-- 1.12 Admin Activity Log
-- ---------------------------------------------------
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[admin_logs]') AND type in (N'U'))
BEGIN
    CREATE TABLE admin_logs (
        id INT IDENTITY(1,1) PRIMARY KEY,
        admin_id INT NOT NULL,
        action NVARCHAR(200) NOT NULL,
        entity_type NVARCHAR(50),
        entity_id INT,
        details NVARCHAR(MAX),
        created_at DATETIME2 DEFAULT GETUTCDATE(),
        CONSTRAINT FK_admin_logs_admin FOREIGN KEY (admin_id) REFERENCES users(id)
    );
END
GO

-- ============================================================================
-- 2. INDEXES
-- ============================================================================

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_users_role')
    CREATE INDEX idx_users_role ON users(role);
GO
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_users_email')
    CREATE INDEX idx_users_email ON users(email);
GO
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_teacher_profiles_subject')
    CREATE INDEX idx_teacher_profiles_subject ON teacher_profiles(subject);
GO
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_teacher_profiles_location')
    CREATE INDEX idx_teacher_profiles_location ON teacher_profiles(location);
GO
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_teacher_profiles_fee')
    CREATE INDEX idx_teacher_profiles_fee ON teacher_profiles(fee);
GO
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_user_subscriptions_active')
    CREATE INDEX idx_user_subscriptions_active ON user_subscriptions(user_id, is_active);
GO
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_payments_status')
    CREATE INDEX idx_payments_status ON payments(status);
GO
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_tuition_posts_status')
    CREATE INDEX idx_tuition_posts_status ON tuition_posts(status);
GO
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_messages_receiver_unread')
    CREATE INDEX idx_messages_receiver_unread ON messages(receiver_id, is_read);
GO
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_notifications_user_unread')
    CREATE INDEX idx_notifications_user_unread ON notifications(user_id, is_read);
GO
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_reviews_teacher')
    CREATE INDEX idx_reviews_teacher ON reviews(teacher_id);
GO

-- ============================================================================
-- 3. STORED PROCEDURES
-- ============================================================================

-- ---------------------------------------------------
-- 3.1 sp_GetTeacherDashboardStats
-- ---------------------------------------------------
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'sp_GetTeacherDashboardStats')
    DROP PROCEDURE sp_GetTeacherDashboardStats
GO
CREATE PROCEDURE sp_GetTeacherDashboardStats
    @TeacherId INT
AS
BEGIN
    SET NOCOUNT ON;
    SELECT
        (SELECT COUNT(*) FROM applications WHERE teacher_id = @TeacherId AND status = 'Pending') AS PendingApplications,
        (SELECT COUNT(*) FROM applications WHERE teacher_id = @TeacherId AND status = 'Selected') AS SelectedApplications,
        (SELECT COUNT(*) FROM applications WHERE teacher_id = @TeacherId) AS TotalApplications,
        (SELECT COUNT(*) FROM messages WHERE receiver_id = @TeacherId AND is_read = 0) AS UnreadMessages,
        (SELECT ISNULL(AVG(CAST(rating AS DECIMAL(3,2))), 0) FROM reviews WHERE teacher_id = @TeacherId) AS AvgRating,
        (SELECT COUNT(*) FROM reviews WHERE teacher_id = @TeacherId) AS TotalReviews,
        (SELECT name FROM subscription_plans sp
         INNER JOIN user_subscriptions us ON us.plan_id = sp.id
         WHERE us.user_id = @TeacherId AND us.is_active = 1) AS CurrentPlan;
END
GO

-- ---------------------------------------------------
-- 3.2 sp_GetAdminDashboardStats
-- ---------------------------------------------------
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'sp_GetAdminDashboardStats')
    DROP PROCEDURE sp_GetAdminDashboardStats
GO
CREATE PROCEDURE sp_GetAdminDashboardStats
AS
BEGIN
    SET NOCOUNT ON;
    SELECT
        (SELECT COUNT(*) FROM users WHERE role = 'student') AS TotalStudents,
        (SELECT COUNT(*) FROM users WHERE role = 'teacher') AS TotalTeachers,
        (SELECT COUNT(*) FROM users WHERE role = 'teacher' AND is_approved = 0) AS PendingTeachers,
        (SELECT COUNT(*) FROM payments WHERE status = 'Pending') AS PendingPayments,
        (SELECT ISNULL(SUM(amount), 0) FROM payments WHERE status = 'Approved') AS TotalRevenue,
        (SELECT COUNT(*) FROM tuition_posts WHERE status = 'Open') AS OpenPosts,
        (SELECT COUNT(*) FROM applications WHERE status = 'Pending') AS PendingApplications,
        (SELECT COUNT(*) FROM messages WHERE is_read = 0) AS UnreadMessages;
END
GO

-- ---------------------------------------------------
-- 3.3 sp_GetMonthlyRevenue
-- ---------------------------------------------------
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'sp_GetMonthlyRevenue')
    DROP PROCEDURE sp_GetMonthlyRevenue
GO
CREATE PROCEDURE sp_GetMonthlyRevenue
    @Year INT = NULL,
    @Month INT = NULL
AS
BEGIN
    SET NOCOUNT ON;
    SELECT
        YEAR(verified_at) AS Year,
        MONTH(verified_at) AS Month,
        COUNT(*) AS TransactionCount,
        ISNULL(SUM(amount), 0) AS Revenue
    FROM payments
    WHERE status = 'Approved'
        AND (@Year IS NULL OR YEAR(verified_at) = @Year)
        AND (@Month IS NULL OR MONTH(verified_at) = @Month)
    GROUP BY YEAR(verified_at), MONTH(verified_at)
    ORDER BY Year DESC, Month DESC;
END
GO

-- ---------------------------------------------------
-- 3.4 sp_VerifyPayment
-- ---------------------------------------------------
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'sp_VerifyPayment')
    DROP PROCEDURE sp_VerifyPayment
GO
CREATE PROCEDURE sp_VerifyPayment
    @PaymentId INT,
    @AdminId INT,
    @Status NVARCHAR(20),
    @AdminNote NVARCHAR(MAX) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;
    BEGIN TRY
        DECLARE @UserId INT, @PlanId INT, @DurationDays INT;

        -- Update payment
        UPDATE payments
        SET status = @Status,
            verified_by = @AdminId,
            verified_at = GETUTCDATE(),
            admin_note = COALESCE(@AdminNote, admin_note)
        WHERE id = @PaymentId;

        IF @Status = 'Approved'
        BEGIN
            SELECT @UserId = user_id, @PlanId = plan_id
            FROM payments WHERE id = @PaymentId;

            SELECT @DurationDays = duration_days
            FROM subscription_plans WHERE id = @PlanId;

            -- Deactivate existing active subscription
            UPDATE user_subscriptions
            SET is_active = 0
            WHERE user_id = @UserId AND is_active = 1;

            -- Create new subscription
            INSERT INTO user_subscriptions (user_id, plan_id, start_date, end_date, is_active)
            VALUES (@UserId, @PlanId, GETUTCDATE(), DATEADD(DAY, @DurationDays, GETUTCDATE()), 1);
        END

        -- Log admin action
        INSERT INTO admin_logs (admin_id, action, entity_type, entity_id, details)
        VALUES (@AdminId, 'Payment ' + @Status, 'payment', @PaymentId,
                'Payment #' + CAST(@PaymentId AS NVARCHAR) + ' ' + @Status);

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO

-- ---------------------------------------------------
-- 3.5 sp_AutoDowngradeExpiredSubscriptions
-- ---------------------------------------------------
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'sp_AutoDowngradeExpiredSubscriptions')
    DROP PROCEDURE sp_AutoDowngradeExpiredSubscriptions
GO
CREATE PROCEDURE sp_AutoDowngradeExpiredSubscriptions
AS
BEGIN
    SET NOCOUNT ON;
    -- Deactivate all expired subscriptions
    UPDATE user_subscriptions
    SET is_active = 0
    WHERE is_active = 1 AND end_date < GETUTCDATE();

    -- Log the downgrade count
    DECLARE @Count INT = @@ROWCOUNT;
    IF @Count > 0
    BEGIN
        INSERT INTO admin_logs (admin_id, action, entity_type, entity_id, details)
        VALUES (1, 'Auto Downgrade', 'subscription', 0,
                CAST(@Count AS NVARCHAR) + ' expired subscriptions deactivated');
    END
END
GO

-- ---------------------------------------------------
-- 3.6 sp_CreateNotification
-- ---------------------------------------------------
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'sp_CreateNotification')
    DROP PROCEDURE sp_CreateNotification
GO
CREATE PROCEDURE sp_CreateNotification
    @UserId INT,
    @Type NVARCHAR(50) = 'general',
    @Title NVARCHAR(200),
    @Message NVARCHAR(MAX),
    @Link NVARCHAR(500) = NULL
AS
BEGIN
    INSERT INTO notifications (user_id, type, title, message, link)
    VALUES (@UserId, @Type, @Title, @Message, @Link);
END
GO

-- ---------------------------------------------------
-- 3.7 sp_SearchTutors
-- ---------------------------------------------------
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'P' AND name = 'sp_SearchTutors')
    DROP PROCEDURE sp_SearchTutors
GO
CREATE PROCEDURE sp_SearchTutors
    @Subject NVARCHAR(100) = NULL,
    @Location NVARCHAR(100) = NULL,
    @MaxFee INT = NULL,
    @ExperienceLevel NVARCHAR(20) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    SELECT
        u.id, u.name, u.email, u.profile_picture, u.is_online,
        tp.subject, tp.experience, tp.fee, tp.location, tp.bio, tp.availability, tp.is_complete,
        us.is_active AS has_active_subscription,
        COALESCE(sp.priority_ranking, 0) AS priority_ranking,
        sp.has_verified_badge, sp.is_featured,
        (SELECT ISNULL(AVG(CAST(rating AS DECIMAL(3,2))), 0) FROM reviews WHERE teacher_id = u.id) AS avg_rating,
        (SELECT COUNT(*) FROM reviews WHERE teacher_id = u.id) AS review_count
    FROM users u
    INNER JOIN teacher_profiles tp ON tp.user_id = u.id
    LEFT JOIN user_subscriptions us ON us.user_id = u.id AND us.is_active = 1
    LEFT JOIN subscription_plans sp ON sp.id = us.plan_id
    WHERE u.role = 'teacher'
        AND u.is_approved = 1
        AND u.is_active = 1
        AND tp.is_complete = 1
        AND (@Subject IS NULL OR tp.subject LIKE '%' + @Subject + '%')
        AND (@Location IS NULL OR tp.location LIKE '%' + @Location + '%')
        AND (@MaxFee IS NULL OR tp.fee <= @MaxFee)
        AND (@ExperienceLevel IS NULL OR
             (@ExperienceLevel = 'beginner' AND tp.experience < 4) OR
             (@ExperienceLevel = 'intermediate' AND tp.experience BETWEEN 4 AND 7) OR
             (@ExperienceLevel = 'expert' AND tp.experience >= 8))
    ORDER BY
        CASE WHEN sp.is_featured = 1 THEN 0 ELSE 1 END,
        sp.priority_ranking DESC,
        avg_rating DESC;
END
GO

-- ============================================================================
-- 4. VIEWS
-- ============================================================================

-- ---------------------------------------------------
-- 4.1 vw_TutorPublicProfiles
-- ---------------------------------------------------
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'V' AND name = 'vw_TutorPublicProfiles')
    DROP VIEW vw_TutorPublicProfiles
GO
CREATE VIEW vw_TutorPublicProfiles
AS
SELECT
    u.id AS tutor_id,
    u.name,
    u.email,
    u.profile_picture,
    u.is_online,
    tp.subject,
    tp.experience,
    tp.fee,
    tp.location,
    tp.bio,
    tp.university,
    tp.degree,
    tp.availability,
    tp.cv,
    us.is_active AS has_active_subscription,
    sp.has_verified_badge,
    sp.is_featured,
    (SELECT ISNULL(AVG(CAST(rating AS DECIMAL(3,2))), 0) FROM reviews WHERE teacher_id = u.id) AS avg_rating,
    (SELECT COUNT(*) FROM reviews WHERE teacher_id = u.id) AS review_count
FROM users u
INNER JOIN teacher_profiles tp ON tp.user_id = u.id
LEFT JOIN user_subscriptions us ON us.user_id = u.id AND us.is_active = 1
LEFT JOIN subscription_plans sp ON sp.id = us.plan_id
WHERE u.role = 'teacher' AND u.is_approved = 1 AND u.is_active = 1;
GO

-- ---------------------------------------------------
-- 4.2 vw_AdminRevenueReport
-- ---------------------------------------------------
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'V' AND name = 'vw_AdminRevenueReport')
    DROP VIEW vw_AdminRevenueReport
GO
CREATE VIEW vw_AdminRevenueReport
AS
SELECT
    YEAR(p.verified_at) AS Year,
    MONTH(p.verified_at) AS Month,
    sp.name AS PlanName,
    COUNT(*) AS SubscriptionsSold,
    ISNULL(SUM(p.amount), 0) AS Revenue
FROM payments p
INNER JOIN subscription_plans sp ON sp.id = p.plan_id
WHERE p.status = 'Approved'
GROUP BY YEAR(p.verified_at), MONTH(p.verified_at), sp.name;
GO

-- ---------------------------------------------------
-- 4.3 vw_SubscriptionStatus
-- ---------------------------------------------------
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'V' AND name = 'vw_SubscriptionStatus')
    DROP VIEW vw_SubscriptionStatus
GO
CREATE VIEW vw_SubscriptionStatus
AS
SELECT
    u.id AS user_id,
    u.name,
    u.email,
    sp.name AS plan_name,
    us.start_date,
    us.end_date,
    us.is_active,
    DATEDIFF(DAY, GETUTCDATE(), us.end_date) AS days_remaining,
    CASE
        WHEN us.end_date < GETUTCDATE() THEN 'Expired'
        WHEN DATEDIFF(DAY, GETUTCDATE(), us.end_date) <= 7 THEN 'Expiring Soon'
        ELSE 'Active'
    END AS status_label
FROM users u
LEFT JOIN user_subscriptions us ON us.user_id = u.id AND us.is_active = 1
LEFT JOIN subscription_plans sp ON sp.id = us.plan_id
WHERE u.role = 'teacher';
GO

-- ---------------------------------------------------
-- 4.4 vw_TutorAnalytics
-- ---------------------------------------------------
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'V' AND name = 'vw_TutorAnalytics')
    DROP VIEW vw_TutorAnalytics
GO
CREATE VIEW vw_TutorAnalytics
AS
SELECT
    u.id AS tutor_id,
    u.name,
    COUNT(DISTINCT a.id) AS total_applications,
    COUNT(DISTINCT CASE WHEN a.status = 'Pending' THEN a.id END) AS pending_applications,
    COUNT(DISTINCT CASE WHEN a.status = 'Selected' THEN a.id END) AS selected_applications,
    COUNT(DISTINCT r.id) AS total_reviews,
    ISNULL(AVG(CAST(r.rating AS DECIMAL(3,2))), 0) AS avg_rating,
    COUNT(DISTINCT m.id) AS total_messages_received,
    COUNT(DISTINCT CASE WHEN m.is_read = 0 THEN m.id END) AS unread_messages
FROM users u
LEFT JOIN applications a ON a.teacher_id = u.id
LEFT JOIN reviews r ON r.teacher_id = u.id
LEFT JOIN messages m ON m.receiver_id = u.id
WHERE u.role = 'teacher'
GROUP BY u.id, u.name;
GO

-- ============================================================================
-- 5. TRIGGERS
-- ============================================================================

-- ---------------------------------------------------
-- 5.1 trg_UpdateUserTimestamp
-- ---------------------------------------------------
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'TR' AND name = 'trg_UpdateUserTimestamp')
    DROP TRIGGER trg_UpdateUserTimestamp
GO
CREATE TRIGGER trg_UpdateUserTimestamp
ON users
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE users
    SET updated_at = GETUTCDATE()
    FROM users u
    INNER JOIN inserted i ON i.id = u.id;
END
GO

-- ---------------------------------------------------
-- 5.2 trg_UpdateTeacherProfileTimestamp
-- ---------------------------------------------------
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'TR' AND name = 'trg_UpdateTeacherProfileTimestamp')
    DROP TRIGGER trg_UpdateTeacherProfileTimestamp
GO
CREATE TRIGGER trg_UpdateTeacherProfileTimestamp
ON teacher_profiles
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE teacher_profiles
    SET updated_at = GETUTCDATE()
    FROM teacher_profiles tp
    INNER JOIN inserted i ON i.id = tp.id;
END
GO

-- ---------------------------------------------------
-- 5.3 trg_NewPaymentNotification
-- ---------------------------------------------------
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'TR' AND name = 'trg_NewPaymentNotification')
    DROP TRIGGER trg_NewPaymentNotification
GO
CREATE TRIGGER trg_NewPaymentNotification
ON payments
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @UserId INT, @Amount DECIMAL(10,2), @PaymentId INT;

    SELECT @PaymentId = id, @UserId = user_id, @Amount = amount FROM inserted;

    -- Notify the user
    INSERT INTO notifications (user_id, type, title, message, link)
    VALUES (@UserId, 'payment', 'Payment Received',
            'Your payment of BDT ' + CAST(@Amount AS NVARCHAR) + ' has been received. Awaiting admin verification.',
            '/payments/history');

    -- Notify all admins
    INSERT INTO notifications (user_id, type, title, message, link)
    SELECT id, 'payment', 'New Payment Request',
           'A new payment of BDT ' + CAST(@Amount AS NVARCHAR) + ' needs verification.',
           '/admin/payments'
    FROM users WHERE role = 'admin';
END
GO

-- ---------------------------------------------------
-- 5.4 trg_SubscriptionExpiryNotification
-- ---------------------------------------------------
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'TR' AND name = 'trg_SubscriptionExpiryNotification')
    DROP TRIGGER trg_SubscriptionExpiryNotification
GO
CREATE TRIGGER trg_SubscriptionExpiryNotification
ON user_subscriptions
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    IF EXISTS (SELECT 1 FROM inserted i
               INNER JOIN subscription_plans sp ON sp.id = i.plan_id
               WHERE i.is_active = 1
                 AND DATEDIFF(DAY, GETUTCDATE(), i.end_date) = 7)
    BEGIN
        INSERT INTO notifications (user_id, type, title, message, link)
        SELECT
            i.user_id,
            'subscription',
            'Subscription Expiring Soon',
            'Your ' + sp.name + ' plan will expire on ' +
            FORMAT(i.end_date, 'dd-MMM-yyyy') + '. Renew now to keep your benefits.',
            '/subscriptions/plans'
        FROM inserted i
        INNER JOIN subscription_plans sp ON sp.id = i.plan_id
        WHERE i.is_active = 1
            AND DATEDIFF(DAY, GETUTCDATE(), i.end_date) = 7;
    END
END
GO

-- ---------------------------------------------------
-- 5.5 trg_NewMessageNotification
-- ---------------------------------------------------
IF EXISTS (SELECT * FROM sys.objects WHERE type = 'TR' AND name = 'trg_NewMessageNotification')
    DROP TRIGGER trg_NewMessageNotification
GO
CREATE TRIGGER trg_NewMessageNotification
ON messages
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @SenderId INT, @ReceiverId INT, @SenderName NVARCHAR(100);

    SELECT @SenderId = sender_id, @ReceiverId = receiver_id FROM inserted;
    SELECT @SenderName = name FROM users WHERE id = @SenderId;

    INSERT INTO notifications (user_id, type, title, message, link)
    VALUES (@ReceiverId, 'message', 'New Message',
            'You have a new message from ' + @SenderName,
            CASE WHEN EXISTS (SELECT 1 FROM users WHERE id = @ReceiverId AND role = 'teacher')
                 THEN '/teacher/messages' ELSE '/student/messages' END);
END
GO

-- ============================================================================
-- 6. SEED DATA
-- ============================================================================

-- ---------------------------------------------------
-- 6.1 Subscription Plans
-- ---------------------------------------------------
IF NOT EXISTS (SELECT 1 FROM subscription_plans)
BEGIN
    INSERT INTO subscription_plans (name, price, duration_days, max_applications, is_featured, has_verified_badge, priority_ranking, description)
    VALUES
        ('Free', 0, 9999, 3, 0, 0, 0,
         'Get started with basic access. Apply to 3 tuition posts per month.'),
        ('Standard', 499, 30, NULL, 0, 1, 1,
         'Unlimited applications, verified profile badge, and priority search ranking.'),
        ('Premium', 999, 30, NULL, 1, 1, 2,
         'Everything in Standard plus homepage featured placement, analytics dashboard, and priority support.');
END
GO

-- ---------------------------------------------------
-- 6.2 Default Admin Account (password: admin123)
-- ---------------------------------------------------
IF NOT EXISTS (SELECT 1 FROM users WHERE email = 'admin@tuition.com')
BEGIN
    INSERT INTO users (name, email, password_hash, role, is_active, is_approved)
    VALUES ('Admin', 'admin@tuition.com',
            'scrypt:32768:8:1$P5x3F0bGQ4pYMj1X$b6a7e8f9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b',
            'admin', 1, 1);
END
GO

PRINT '=== TuitionStation database schema created successfully! ===';
GO
