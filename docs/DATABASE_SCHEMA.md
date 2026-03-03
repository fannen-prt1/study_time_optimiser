# Database Schema Documentation

## Overview

The Study Time Optimizer uses a relational database (SQLite for development, PostgreSQL for production) managed via **SQLAlchemy ORM** with **Alembic** migrations.

### Entities

| Table | Description |
|-------|-------------|
| users | User accounts and profiles |
| subjects | Subjects/courses a user studies |
| study_sessions | Individual study session records |
| goals | Daily/weekly/monthly study targets |
| deadlines | Exam and assignment due dates |
| daily_wellness | Daily wellness & sleep tracking |
| study_streaks | Consecutive study day tracking |
| refresh_tokens | JWT refresh token storage |
| achievements | Earned badges (model exists, not actively used in API) |
| pomodoro_sessions | Pomodoro intervals (model exists, not actively used in API) |
| ai_predictions | AI prediction logs (model exists, not actively used in API) |

---

## Entity Relationship Diagram

```
┌────────────────┐
│     users      │
└───────┬────────┘
        │
        ├──────────┬─────────────┬───────────┬──────────────┬───────────────┬──────────────┬───────────────┬──────────────┐
        │          │             │           │              │               │              │               │              │
        ▼          ▼             ▼           ▼              ▼               ▼              ▼               ▼              ▼
   ┌─────────┐ ┌──────────┐ ┌──────┐ ┌──────────┐ ┌──────────────┐ ┌──────────┐ ┌───────────────┐ ┌──────────────┐ ┌──────────────┐
   │subjects │ │ sessions │ │goals │ │deadlines │ │daily_wellness│ │ streaks  │ │refresh_tokens │ │ achievements │ │ai_predictions│
   └────┬────┘ └──────────┘ └──────┘ └──────────┘ └──────────────┘ └──────────┘ └───────────────┘ └──────────────┘ └──────────────┘
        │          │                                                                                      │
        │          └──────────────────────────────────────────────────────────────────────────────────────┐│
        │                                                                                                 ▼
        │                                                                                        ┌──────────────────┐
        └───────────────────────────────────────────────────────────────────────────────────────▶│pomodoro_sessions │
                                                                                                 └──────────────────┘
```

- `subjects` ← FK from `study_sessions`, `goals`, `deadlines`
- `study_sessions` ← FK from `pomodoro_sessions`

---

## Tables

### 1. users

Stores user account information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT | PRIMARY KEY | UUID |
| email | TEXT | UNIQUE, NOT NULL, INDEX | User email |
| password_hash | TEXT | NOT NULL | Bcrypt hash |
| full_name | TEXT | NOT NULL | Display name |
| age | INTEGER | NULLABLE | User's age |
| student_type | TEXT | NOT NULL | `high_school`, `college`, `graduate`, `professional` |
| profile_image_url | TEXT | NULLABLE | Avatar URL |
| is_active | BOOLEAN | DEFAULT TRUE | Account active? |
| is_verified | BOOLEAN | DEFAULT FALSE | Email verified? |
| verification_code | VARCHAR(6) | NULLABLE | 6-digit email verification code |
| verification_code_expires | TIMESTAMP | NULLABLE | Code expiry time |
| reset_password_token | TEXT | NULLABLE | Password reset token |
| reset_password_expires | TIMESTAMP | NULLABLE | Reset token expiry |
| created_at | TIMESTAMP | DEFAULT NOW | Created |
| updated_at | TIMESTAMP | DEFAULT NOW, ON UPDATE | Updated |
| last_login | TIMESTAMP | NULLABLE | Last login time |

**Relationships:** Has many subjects, study_sessions, goals, deadlines, achievements, wellness_entries, refresh_tokens, ai_predictions. Has one study_streak.

---

### 2. subjects

Subjects/courses the user studies.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT | PRIMARY KEY | UUID |
| user_id | TEXT | NOT NULL, FK → users.id (CASCADE), INDEX | Owner |
| name | TEXT | NOT NULL | Subject name |
| color | TEXT | DEFAULT '#0ea5e9' | Hex color for UI |
| icon | TEXT | DEFAULT '📚' | Emoji icon |
| description | TEXT | NULLABLE | Description |
| is_archived | BOOLEAN | DEFAULT FALSE | Archived? |
| created_at | TIMESTAMP | DEFAULT NOW, INDEX | Created |
| updated_at | TIMESTAMP | DEFAULT NOW, ON UPDATE | Updated |

**Relationships:** Has many study_sessions, goals, deadlines. Belongs to user.

---

### 3. study_sessions

Core table for study session tracking.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT | PRIMARY KEY | UUID |
| user_id | TEXT | NOT NULL, FK → users.id (CASCADE), INDEX | Owner |
| subject_id | TEXT | NOT NULL, FK → subjects.id (CASCADE), INDEX | Subject studied |
| session_type | TEXT | NOT NULL | `focused_study`, `practice`, `reading`, `review` |
| status | TEXT | DEFAULT 'active', INDEX | `active`, `paused`, `completed`, `cancelled` |
| start_time | TIMESTAMP | NOT NULL, INDEX | Session start |
| end_time | TIMESTAMP | NULLABLE | Session end |
| planned_duration_minutes | INTEGER | NULLABLE | Planned length |
| actual_duration_minutes | INTEGER | NULLABLE | Actual length |
| pause_count | INTEGER | DEFAULT 0 | Number of pauses |
| total_pause_duration_minutes | INTEGER | DEFAULT 0 | Total pause time |
| productivity_score | INTEGER | NULLABLE (0–100) | Self-reported productivity |
| focus_score | INTEGER | NULLABLE (0–100) | Self-reported focus |
| energy_level | INTEGER | NULLABLE (1–5) | Energy rating |
| difficulty_level | INTEGER | NULLABLE (1–5) | Difficulty rating |
| satisfaction_level | INTEGER | NULLABLE (1–5) | Satisfaction rating |
| notes | TEXT | NULLABLE | Session notes |
| created_at | TIMESTAMP | DEFAULT NOW | Created |
| updated_at | TIMESTAMP | DEFAULT NOW, ON UPDATE | Updated |

**Relationships:** Belongs to user and subject. Has many pomodoro_sessions.

---

### 4. goals

Study goals (daily, weekly, monthly).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT | PRIMARY KEY | UUID |
| user_id | TEXT | NOT NULL, FK → users.id (CASCADE), INDEX | Owner |
| subject_id | TEXT | NULLABLE, FK → subjects.id (SET NULL) | Optional subject |
| goal_type | TEXT | NOT NULL, INDEX | `daily`, `weekly`, `monthly` |
| target_hours | INTEGER | NOT NULL | Target hours |
| start_date | DATE | NOT NULL, INDEX | Period start |
| end_date | DATE | NOT NULL | Period end |
| current_hours | FLOAT | DEFAULT 0.0 | Progress |
| is_achieved | BOOLEAN | DEFAULT FALSE | Achieved? |
| achieved_at | TIMESTAMP | NULLABLE | Achievement time |
| created_at | TIMESTAMP | DEFAULT NOW | Created |
| updated_at | TIMESTAMP | DEFAULT NOW, ON UPDATE | Updated |

---

### 5. deadlines

Exam and assignment deadlines.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT | PRIMARY KEY | UUID |
| user_id | TEXT | NOT NULL, FK → users.id (CASCADE), INDEX | Owner |
| subject_id | TEXT | NOT NULL, FK → subjects.id (CASCADE) | Related subject |
| title | TEXT | NOT NULL | Deadline title |
| description | TEXT | NULLABLE | Details |
| deadline_date | TIMESTAMP | NOT NULL, INDEX | Due date/time |
| priority | TEXT | DEFAULT 'medium', INDEX | `low`, `medium`, `high`, `urgent` |
| is_completed | BOOLEAN | DEFAULT FALSE | Done? |
| completed_at | TIMESTAMP | NULLABLE | Completion time |
| reminder_sent | BOOLEAN | DEFAULT FALSE | Reminder sent? |
| created_at | TIMESTAMP | DEFAULT NOW | Created |
| updated_at | TIMESTAMP | DEFAULT NOW, ON UPDATE | Updated |

---

### 6. daily_wellness

Daily wellness and sleep tracking. One entry per user per day.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT | PRIMARY KEY | UUID |
| user_id | TEXT | NOT NULL, FK → users.id (CASCADE), INDEX | Owner |
| date | DATE | NOT NULL, INDEX | Entry date |
| sleep_hours | FLOAT | NULLABLE (0–24) | Hours slept |
| sleep_quality | INTEGER | NULLABLE (1–5) | Sleep quality |
| energy_level | INTEGER | NULLABLE (1–5) | Energy level |
| stress_level | INTEGER | NULLABLE (1–10) | Stress level |
| mood | INTEGER | NULLABLE (1–5) | Mood rating |
| focus_score | INTEGER | NULLABLE (1–100) | Focus rating |
| notes | TEXT | NULLABLE | Notes |
| created_at | TIMESTAMP | DEFAULT NOW | Created |
| updated_at | TIMESTAMP | DEFAULT NOW, ON UPDATE | Updated |

**Unique Constraint:** `(user_id, date)` — one entry per user per day.

---

### 7. study_streaks

Tracks consecutive study days. One row per user.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT | PRIMARY KEY | UUID |
| user_id | TEXT | NOT NULL, FK → users.id (CASCADE), UNIQUE, INDEX | Owner |
| current_streak | INTEGER | DEFAULT 0 | Consecutive days |
| longest_streak | INTEGER | DEFAULT 0 | All-time record |
| last_study_date | DATE | NULLABLE | Last study date |
| created_at | TIMESTAMP | DEFAULT NOW | Created |
| updated_at | TIMESTAMP | DEFAULT NOW, ON UPDATE | Updated |

---

### 8. refresh_tokens

JWT refresh tokens for authentication.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT | PRIMARY KEY | UUID |
| user_id | TEXT | NOT NULL, FK → users.id (CASCADE), INDEX | Owner |
| token | TEXT | UNIQUE, NOT NULL, INDEX | The refresh token |
| expires_at | TIMESTAMP | NOT NULL | Token expiry |
| is_revoked | BOOLEAN | DEFAULT FALSE | Revoked? |
| created_at | TIMESTAMP | DEFAULT NOW | Created |

---

### 9. achievements

Badges and achievements (model exists; no dedicated API router).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT | PRIMARY KEY | UUID |
| user_id | TEXT | NOT NULL, FK → users.id (CASCADE), INDEX | Owner |
| badge_type | TEXT | NOT NULL | Badge identifier |
| earned_at | TIMESTAMP | DEFAULT NOW, INDEX | Earned time |
| description | TEXT | NULLABLE | Description |

**Unique Constraint:** `(user_id, badge_type)` — no duplicate badges.

---

### 10. pomodoro_sessions

Pomodoro intervals within study sessions (model exists; no dedicated API router).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT | PRIMARY KEY | UUID |
| study_session_id | TEXT | NOT NULL, FK → study_sessions.id (CASCADE), INDEX | Parent session |
| pomodoro_number | INTEGER | NOT NULL | Sequence number |
| duration_minutes | INTEGER | DEFAULT 25 | Work duration |
| break_duration_minutes | INTEGER | DEFAULT 5 | Break duration |
| completed | BOOLEAN | DEFAULT FALSE | Completed? |
| created_at | TIMESTAMP | DEFAULT NOW | Created |

---

### 11. ai_predictions

AI model prediction logs (model exists; no dedicated API router for persistence).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | TEXT | PRIMARY KEY | UUID |
| user_id | TEXT | NOT NULL, FK → users.id (CASCADE), INDEX | Owner |
| prediction_type | TEXT | NOT NULL, INDEX | `productivity`, `optimal_time`, `duration` |
| subject_id | TEXT | NULLABLE | Subject context |
| time_slot | INTEGER | NULLABLE | Hour of day (0–23) |
| predicted_value | FLOAT | NOT NULL | Predicted value |
| confidence_score | FLOAT | NULLABLE | Confidence (0–1) |
| model_version | TEXT | NULLABLE | Model version |
| created_at | TIMESTAMP | DEFAULT NOW | Created |

---

## Migration Strategy

Using **Alembic** for database migrations:

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one step
alembic downgrade -1
```

---

## Example Queries

### User's total study time this week
```sql
SELECT SUM(actual_duration_minutes) / 60.0 AS total_hours
FROM study_sessions
WHERE user_id = 'user_uuid'
  AND start_time >= date('now', 'weekday 0', '-7 days')
  AND status = 'completed';
```

### Subject with most study time
```sql
SELECT s.name, SUM(ss.actual_duration_minutes) / 60.0 AS hours
FROM study_sessions ss
JOIN subjects s ON ss.subject_id = s.id
WHERE ss.user_id = 'user_uuid' AND ss.status = 'completed'
GROUP BY s.id, s.name
ORDER BY hours DESC
LIMIT 1;
```

### Daily productivity trend (last 30 days)
```sql
SELECT DATE(start_time) AS date, AVG(productivity_score) AS avg_productivity
FROM study_sessions
WHERE user_id = 'user_uuid'
  AND status = 'completed'
  AND productivity_score IS NOT NULL
GROUP BY DATE(start_time)
ORDER BY date DESC
LIMIT 30;
```
