-- Database Initialization Script
-- Run this to set up a fresh database

-- Drop existing tables (use with caution!)
-- DROP TABLE IF EXISTS pomodoro_sessions;
-- DROP TABLE IF EXISTS study_streaks;
-- DROP TABLE IF EXISTS achievements;
-- DROP TABLE IF EXISTS ai_predictions;
-- DROP TABLE IF EXISTS deadlines;
-- DROP TABLE IF EXISTS goals;
-- DROP TABLE IF EXISTS study_sessions;
-- DROP TABLE IF EXISTS subjects;
-- DROP TABLE IF EXISTS users;

-- Load schema
\i schema.sql

-- Create default indexes and optimize
VACUUM;
ANALYZE;

-- Success message
SELECT 'Database initialized successfully!' AS status;
