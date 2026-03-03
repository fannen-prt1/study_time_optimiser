-- Study Time Optimizer Database Schema
-- PostgreSQL / SQLite Compatible

-- ============================================
-- USERS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    age INTEGER,
    student_type TEXT CHECK(student_type IN ('high_school', 'college', 'graduate', 'professional')) NOT NULL,
    profile_image_url TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    verification_token TEXT,
    reset_password_token TEXT,
    reset_password_expires TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

-- ============================================
-- SUBJECTS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS subjects (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    name TEXT NOT NULL,
    color TEXT DEFAULT '#0ea5e9',
    icon TEXT DEFAULT '📚',
    description TEXT,
    is_archived BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_subjects_user_id ON subjects(user_id);
CREATE INDEX idx_subjects_created_at ON subjects(created_at);

-- ============================================
-- STUDY SESSIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS study_sessions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    subject_id TEXT NOT NULL,
    session_type TEXT CHECK(session_type IN ('focused_study', 'practice', 'reading', 'review')) NOT NULL,
    status TEXT CHECK(status IN ('active', 'paused', 'completed', 'cancelled')) DEFAULT 'active',
    
    -- Time tracking
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    planned_duration_minutes INTEGER,
    actual_duration_minutes INTEGER,
    pause_count INTEGER DEFAULT 0,
    total_pause_duration_minutes INTEGER DEFAULT 0,
    
    -- Performance metrics
    productivity_score INTEGER CHECK(productivity_score >= 0 AND productivity_score <= 100),
    focus_score INTEGER CHECK(focus_score >= 0 AND focus_score <= 100),
    
    -- Feedback
    energy_level INTEGER CHECK(energy_level >= 1 AND energy_level <= 5),
    difficulty_level INTEGER CHECK(difficulty_level >= 1 AND difficulty_level <= 5),
    satisfaction_level INTEGER CHECK(satisfaction_level >= 1 AND satisfaction_level <= 5),
    notes TEXT,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);

CREATE INDEX idx_sessions_user_id ON study_sessions(user_id);
CREATE INDEX idx_sessions_subject_id ON study_sessions(subject_id);
CREATE INDEX idx_sessions_start_time ON study_sessions(start_time);
CREATE INDEX idx_sessions_status ON study_sessions(status);

-- ============================================
-- GOALS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS goals (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    goal_type TEXT CHECK(goal_type IN ('daily', 'weekly', 'monthly')) NOT NULL,
    target_hours INTEGER NOT NULL,
    subject_id TEXT,
    
    -- Time period
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    
    -- Progress
    current_hours REAL DEFAULT 0,
    is_achieved BOOLEAN DEFAULT FALSE,
    achieved_at TIMESTAMP,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE SET NULL
);

CREATE INDEX idx_goals_user_id ON goals(user_id);
CREATE INDEX idx_goals_start_date ON goals(start_date);
CREATE INDEX idx_goals_goal_type ON goals(goal_type);

-- ============================================
-- DEADLINES TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS deadlines (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    subject_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    deadline_date TIMESTAMP NOT NULL,
    
    -- Priority
    priority TEXT CHECK(priority IN ('low', 'medium', 'high', 'urgent')) DEFAULT 'medium',
    
    -- Status
    is_completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP,
    
    -- Notifications
    reminder_sent BOOLEAN DEFAULT FALSE,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);

CREATE INDEX idx_deadlines_user_id ON deadlines(user_id);
CREATE INDEX idx_deadlines_deadline_date ON deadlines(deadline_date);
CREATE INDEX idx_deadlines_priority ON deadlines(priority);

-- ============================================
-- AI PREDICTIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS ai_predictions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    prediction_type TEXT CHECK(prediction_type IN ('productivity', 'optimal_time', 'duration')) NOT NULL,
    
    -- Input parameters
    subject_id TEXT,
    time_slot INTEGER,
    
    -- Prediction results
    predicted_value REAL NOT NULL,
    confidence_score REAL,
    
    -- Model metadata
    model_version TEXT,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_predictions_user_id ON ai_predictions(user_id);
CREATE INDEX idx_predictions_type ON ai_predictions(prediction_type);

-- ============================================
-- ACHIEVEMENTS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS achievements (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    badge_type TEXT NOT NULL,
    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Metadata
    description TEXT,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id, badge_type)
);

CREATE INDEX idx_achievements_user_id ON achievements(user_id);
CREATE INDEX idx_achievements_earned_at ON achievements(earned_at);

-- ============================================
-- STUDY STREAKS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS study_streaks (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    last_study_date DATE,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id)
);

CREATE INDEX idx_streaks_user_id ON study_streaks(user_id);

-- ============================================
-- POMODORO SESSIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS pomodoro_sessions (
    id TEXT PRIMARY KEY,
    study_session_id TEXT NOT NULL,
    pomodoro_number INTEGER NOT NULL,
    duration_minutes INTEGER DEFAULT 25,
    break_duration_minutes INTEGER DEFAULT 5,
    completed BOOLEAN DEFAULT FALSE,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (study_session_id) REFERENCES study_sessions(id) ON DELETE CASCADE
);

CREATE INDEX idx_pomodoro_session_id ON pomodoro_sessions(study_session_id);

-- ============================================
-- DAILY WELLNESS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS daily_wellness (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    date DATE NOT NULL,
    sleep_hours REAL CHECK(sleep_hours >= 0 AND sleep_hours <= 24),
    sleep_quality INTEGER CHECK(sleep_quality >= 1 AND sleep_quality <= 5),
    energy_level INTEGER CHECK(energy_level >= 1 AND energy_level <= 5),
    stress_level INTEGER CHECK(stress_level >= 1 AND stress_level <= 5),
    mood INTEGER CHECK(mood >= 1 AND mood <= 5),
    notes TEXT,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id, date)
);

CREATE INDEX idx_wellness_user_id ON daily_wellness(user_id);
CREATE INDEX idx_wellness_date ON daily_wellness(date);

-- ============================================
-- REFRESH TOKENS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS refresh_tokens (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    token TEXT UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    is_revoked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_token ON refresh_tokens(token);
