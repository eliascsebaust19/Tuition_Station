SELECT 
    u.id, u.name, tp.experience, tp.subject,
    (SELECT COUNT(*) FROM applications WHERE teacher_id = u.id) as total_apps,
    (SELECT COUNT(*) FROM reviews WHERE teacher_id = u.id) as total_reviews
FROM users u
JOIN teacher_profiles tp ON tp.user_id = u.id
WHERE u.role = 'teacher'
ORDER BY u.id;
