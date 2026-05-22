-- TuitionStation Advanced Database Schema Features
-- Target: Microsoft SQL Server

-- 1. VIEW: Active Premium Tutors
-- Join users, teacher_profiles, and user_subscriptions to show featured tutors
GO
CREATE OR ALTER VIEW vw_ActivePremiumTutors AS
SELECT 
    u.id, u.name, u.email, u.profile_picture,
    tp.subject, tp.experience, tp.fee, tp.location, tp.bio,
    sp.name as plan_name, sp.priority_ranking
FROM users u
JOIN teacher_profiles tp ON u.id = tp.user_id
JOIN user_subscriptions us ON u.id = us.user_id
JOIN subscription_plans sp ON us.plan_id = sp.id
WHERE u.role = 'teacher' 
  AND u.is_approved = 1 
  AND u.is_active = 1
  AND us.is_active = 1
  AND us.end_date > GETDATE()
  AND sp.is_featured = 1;
GO

-- 2. STORED PROCEDURE: Approve Payment and Activate Subscription
-- Handles transaction logic for approving a payment and updating user subscription
GO
CREATE OR ALTER PROCEDURE sp_ApprovePayment
    @PaymentId INT,
    @AdminId INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;
    BEGIN TRY
        DECLARE @UserId INT, @PlanId INT, @DurationDays INT;

        -- Get payment details
        SELECT @UserId = user_id, @PlanId = plan_id FROM payments WHERE id = @PaymentId AND status = 'Pending';

        IF @UserId IS NULL
        BEGIN
            ROLLBACK TRANSACTION;
            PRINT 'Payment not found or already processed.';
            RETURN;
        END

        -- Get plan duration
        SELECT @DurationDays = duration_days FROM subscription_plans WHERE id = @PlanId;

        -- Deactivate old subscriptions
        UPDATE user_subscriptions SET is_active = 0 WHERE user_id = @UserId;

        -- Insert new subscription
        INSERT INTO user_subscriptions (user_id, plan_id, start_date, end_date, is_active)
        VALUES (@UserId, @PlanId, GETDATE(), DATEADD(day, @DurationDays, GETDATE()), 1);

        -- Update payment status
        UPDATE payments SET status = 'Approved', verified_at = GETDATE() WHERE id = @PaymentId;

        -- Add Notification
        INSERT INTO notifications (user_id, title, message, is_read, created_at)
        VALUES (@UserId, 'Subscription Activated', 'Your payment has been verified. Welcome to the ' + (SELECT name FROM subscription_plans WHERE id = @PlanId) + ' plan!', 0, GETDATE());

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO

-- 3. TRIGGER: Prevent Duplicate active subscriptions
-- Ensures a user doesn't have multiple active subscriptions at once
GO
CREATE OR ALTER TRIGGER trg_SingleActiveSubscription
ON user_subscriptions
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE us
    SET us.is_active = 0
    FROM user_subscriptions us
    JOIN inserted i ON us.user_id = i.user_id
    WHERE us.id <> i.id AND us.is_active = 1;
END;
GO
