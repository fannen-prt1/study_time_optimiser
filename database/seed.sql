-- Sample Data for Testing
-- This file contains test data for development purposes

-- Note: Password is 'password123' hashed with bcrypt
-- In production, use proper password hashing

-- Sample Users
INSERT INTO users (id, email, password_hash, full_name, student_type, is_active, is_verified, created_at)
VALUES
    ('user_001', 'demo@studyoptimizer.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewnYuWwH1J3MqQYW', 'Demo Student', 'college', TRUE, TRUE, CURRENT_TIMESTAMP),
    ('user_002', 'john@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewnYuWwH1J3MqQYW', 'John Doe', 'high_school', TRUE, TRUE, CURRENT_TIMESTAMP);

-- Sample Subjects
INSERT INTO subjects (id, user_id, name, color, icon, description, created_at)
VALUES
    ('subj_001', 'user_001', 'Mathematics', '#ef4444', '📐', 'Calculus and Linear Algebra', CURRENT_TIMESTAMP),
    ('subj_002', 'user_001', 'Computer Science', '#3b82f6', '💻', 'Data Structures and Algorithms', CURRENT_TIMESTAMP),
    ('subj_003', 'user_001', 'Physics', '#8b5cf6', '⚛️', 'Classical Mechanics and Thermodynamics', CURRENT_TIMESTAMP),
    ('subj_004', 'user_001', 'English', '#10b981', '📚', 'Literature and Writing', CURRENT_TIMESTAMP),
    ('subj_005', 'user_002', 'Biology', '#22c55e', '🧬', 'Cell Biology and Genetics', CURRENT_TIMESTAMP);

-- Sample Study Sessions (for ML training)
INSERT INTO study_sessions (
    id, user_id, subject_id, session_type, status, 
    start_time, end_time, planned_duration_minutes, actual_duration_minutes,
    productivity_score, focus_score, energy_level, difficulty_level, satisfaction_level
)
VALUES
    -- Mathematics sessions
    ('sess_001', 'user_001', 'subj_001', 'focused_study', 'completed', 
     datetime('now', '-7 days', '+9 hours'), datetime('now', '-7 days', '+10 hours 30 minutes'), 
     90, 90, 85, 88, 4, 4, 5),
    
    ('sess_002', 'user_001', 'subj_001', 'practice', 'completed',
     datetime('now', '-6 days', '+14 hours'), datetime('now', '-6 days', '+15 hours 15 minutes'),
     75, 75, 78, 82, 3, 3, 4),
    
    ('sess_003', 'user_001', 'subj_001', 'review', 'completed',
     datetime('now', '-5 days', '+10 hours'), datetime('now', '-5 days', '+11 hours'),
     60, 60, 90, 92, 5, 2, 5),
    
    -- Computer Science sessions
    ('sess_004', 'user_001', 'subj_002', 'focused_study', 'completed',
     datetime('now', '-7 days', '+16 hours'), datetime('now', '-7 days', '+18 hours'),
     120, 120, 92, 95, 5, 5, 5),
    
    ('sess_005', 'user_001', 'subj_002', 'practice', 'completed',
     datetime('now', '-6 days', '+15 hours'), datetime('now', '-6 days', '+16 hours 30 minutes'),
     90, 90, 88, 90, 4, 4, 4),
    
    -- Physics sessions
    ('sess_006', 'user_001', 'subj_003', 'reading', 'completed',
     datetime('now', '-5 days', '+20 hours'), datetime('now', '-5 days', '+21 hours 30 minutes'),
     90, 90, 72, 75, 3, 4, 3),
    
    ('sess_007', 'user_001', 'subj_003', 'focused_study', 'completed',
     datetime('now', '-4 days', '+9 hours'), datetime('now', '-4 days', '+10 hours 45 minutes'),
     105, 105, 80, 85, 4, 5, 4),
    
    -- English sessions
    ('sess_008', 'user_001', 'subj_004', 'reading', 'completed',
     datetime('now', '-3 days', '+19 hours'), datetime('now', '-3 days', '+20 hours'),
     60, 60, 88, 90, 4, 2, 5),
    
    -- Recent sessions
    ('sess_009', 'user_001', 'subj_002', 'focused_study', 'completed',
     datetime('now', '-1 day', '+10 hours'), datetime('now', '-1 day', '+11 hours 30 minutes'),
     90, 90, 93, 95, 5, 4, 5),
    
    ('sess_010', 'user_001', 'subj_001', 'practice', 'completed',
     datetime('now', '-1 day', '+15 hours'), datetime('now', '-1 day', '+16 hours'),
     60, 60, 85, 87, 4, 3, 4);

-- Sample Goals
INSERT INTO goals (id, user_id, goal_type, target_hours, start_date, end_date, current_hours)
VALUES
    ('goal_001', 'user_001', 'weekly', 20, date('now', 'weekday 0', '-7 days'), date('now', 'weekday 0'), 12.5),
    ('goal_002', 'user_001', 'monthly', 80, date('now', 'start of month'), date('now', 'start of month', '+1 month', '-1 day'), 35.0),
    ('goal_003', 'user_002', 'weekly', 15, date('now', 'weekday 0', '-7 days'), date('now', 'weekday 0'), 8.0);

-- Sample Deadlines
INSERT INTO deadlines (id, user_id, subject_id, title, description, deadline_date, priority)
VALUES
    ('dead_001', 'user_001', 'subj_001', 'Calculus Exam', 'Chapter 1-5 coverage', datetime('now', '+7 days'), 'high'),
    ('dead_002', 'user_001', 'subj_002', 'Algorithm Project', 'Implement sorting algorithms', datetime('now', '+14 days'), 'high'),
    ('dead_003', 'user_001', 'subj_003', 'Physics Lab Report', 'Mechanics experiment writeup', datetime('now', '+3 days'), 'urgent'),
    ('dead_004', 'user_001', 'subj_004', 'Essay Assignment', '1500 words on Shakespeare', datetime('now', '+10 days'), 'medium');

-- Sample Achievements
INSERT INTO achievements (id, user_id, badge_type, description)
VALUES
    ('ach_001', 'user_001', 'first_session', 'Completed your first study session'),
    ('ach_002', 'user_001', 'streak_3_days', 'Studied for 3 consecutive days'),
    ('ach_003', 'user_001', 'streak_7_days', 'Studied for 7 consecutive days');

-- Sample Study Streak
INSERT INTO study_streaks (id, user_id, current_streak, longest_streak, last_study_date)
VALUES
    ('streak_001', 'user_001', 7, 12, date('now', '-1 day')),
    ('streak_002', 'user_002', 3, 5, date('now', '-1 day'));

-- Success message
SELECT 'Sample data inserted successfully!' AS status;
SELECT COUNT(*) || ' users created' FROM users;
SELECT COUNT(*) || ' subjects created' FROM subjects;
SELECT COUNT(*) || ' study sessions created' FROM study_sessions;
SELECT COUNT(*) || ' goals created' FROM goals;
SELECT COUNT(*) || ' deadlines created' FROM deadlines;
