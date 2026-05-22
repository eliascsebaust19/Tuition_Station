UPDATE teacher_profiles SET
    total_students_taught = experience * 6,
    success_percentage = CASE
        WHEN experience >= 10 THEN 92
        WHEN experience >= 8 THEN 88
        WHEN experience >= 6 THEN 85
        WHEN experience >= 4 THEN 80
        ELSE 75
    END,
    teaching_mode = 'both',
    demo_class_available = CASE WHEN experience >= 6 THEN 1 ELSE 0 END,
    languages = 'Bangla, English',
    teaching_style = CASE
        WHEN subject LIKE '%Math%' THEN 'I focus on building strong conceptual foundations through step-by-step problem solving. My teaching emphasizes understanding the "why" behind every formula rather than rote memorization.'
        WHEN subject LIKE '%Physic%' THEN 'I make physics intuitive by connecting theoretical concepts with real-world applications.'
        WHEN subject LIKE '%Chemist%' THEN 'I simplify complex chemical concepts through practical examples and visual aids.'
        WHEN subject LIKE '%Biolo%' THEN 'I teach biology by focusing on interconnected systems rather than isolated facts.'
        WHEN subject LIKE '%Engl%' THEN 'I focus on immersive language learning through conversation, reading comprehension, and structured grammar.'
        WHEN subject LIKE '%Bang%' THEN 'I teach Bangla with emphasis on literature appreciation, grammar precision, and creative writing.'
        WHEN subject LIKE '%Scien%' THEN 'I make science accessible by breaking down complex topics into simple concepts.'
        WHEN subject LIKE '%Class%' THEN 'I create a nurturing learning environment for young students focusing on foundational skills.'
        ELSE 'I adapt my teaching style to each student learning pace focusing on conceptual clarity and regular practice.'
    END,
    key_strengths = CASE
        WHEN subject LIKE '%Math%' THEN 'Concept Clarity, Problem Solving, Exam Strategy, Logical Reasoning'
        WHEN subject LIKE '%Physic%' THEN 'Conceptual Understanding, Numerical Analysis, Visual Learning, Exam Preparation'
        WHEN subject LIKE '%Chemist%' THEN 'Lab Techniques, Reaction Mechanisms, Problem Solving, Concept Simplification'
        WHEN subject LIKE '%Biolo%' THEN 'Diagram-Based Learning, Memory Techniques, System Analysis, MCQ Strategies'
        WHEN subject LIKE '%Engl%' THEN 'Grammar Expertise, Communication Skills, Writing Guidance, Vocabulary Building'
        WHEN subject LIKE '%Bang%' THEN 'Literature Analysis, Grammar Mastery, Creative Writing, Exam Preparation'
        WHEN subject LIKE '%Scien%' THEN 'Concept Clarity, Interactive Learning, Practical Examples, Exam Strategy'
        ELSE 'Concept Clarity, Patience, Regular Assessment, Student-Friendly Approach'
    END,
    why_students_notice = CASE
        WHEN experience >= 8 THEN 'Known for turning complex topics into simple digestible lessons with a focus on long-term academic growth.'
        WHEN experience >= 5 THEN 'Students appreciate the structured approach and consistent mentoring that builds both skills and confidence.'
        ELSE 'Known for a patient and encouraging teaching style that helps students overcome their academic challenges.'
    END,
    preface = CASE
        WHEN experience >= 10 THEN 'With over a decade of teaching experience I have helped hundreds of students achieve their academic goals through personalized mentoring.'
        WHEN experience >= 6 THEN 'An experienced educator dedicated to providing quality tutoring that goes beyond textbooks to build real understanding.'
        ELSE 'A passionate teacher committed to making learning enjoyable and effective for every student.'
    END,
    tuition_experience = 'Extensive experience guiding students through rigorous academic preparation revision routines and concept building across various curricula.'
WHERE total_students_taught IS NULL OR total_students_taught = 0;
GO
PRINT 'Teacher stats updated successfully';
GO
