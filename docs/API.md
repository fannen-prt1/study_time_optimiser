# API Documentation

## Base URL

```
Development: http://localhost:5000/api/v1
Production: https://your-domain.com/api/v1
```

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your_token>
```

Endpoints marked with 🔒 require authentication. Some additionally require email verification (🔒✅).

---

## Health & Root

### Health Check

**GET** `/health`

```json
{
  "status": "healthy",
  "service": "Study Time Optimizer API",
  "version": "1.0.0",
  "environment": "development"
}
```

### Root

**GET** `/`

```json
{
  "message": "Welcome to Study Time Optimizer API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

---

## Authentication Endpoints

Prefix: `/auth`

### Register

**POST** `/auth/register`

Create a new user account.

**Request Body:**
```json
{
  "email": "student@example.com",
  "password": "SecurePass123",
  "full_name": "John Doe",
  "student_type": "college",
  "age": 21
}
```

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| email | string | yes | Valid email format |
| password | string | yes | Min 8 chars, must contain uppercase, lowercase, and digit |
| full_name | string | yes | 2–100 characters |
| student_type | string | yes | `high_school`, `college`, `graduate`, or `professional` |
| age | integer | no | 13–120 |

**Response (201 Created):**
```json
{
  "id": "uuid",
  "email": "student@example.com",
  "full_name": "John Doe",
  "student_type": "college",
  "age": 21,
  "is_active": true,
  "is_verified": false,
  "created_at": "2026-02-27T10:00:00",
  "updated_at": "2026-02-27T10:00:00",
  "last_login": null
}
```

---

### Login

**POST** `/auth/login`

Authenticate and receive tokens (form-encoded).

**Request Body** (`application/x-www-form-urlencoded`):

| Field | Type | Required |
|-------|------|----------|
| username | string | yes (email) |
| password | string | yes |

**Response (200 OK):**
```json
{
  "access_token": "jwt_token_here",
  "refresh_token": "refresh_token_here",
  "token_type": "bearer",
  "expires_in": 1800
}
```

---

### Refresh Token

**POST** `/auth/refresh`

Get a new access token using a refresh token.

**Request Body:**
```json
{
  "refresh_token": "your_refresh_token"
}
```

**Response (200 OK):**
```json
{
  "access_token": "new_jwt_token",
  "refresh_token": "new_refresh_token",
  "token_type": "bearer",
  "expires_in": 1800
}
```

---

### Logout

**POST** `/auth/logout` 🔒

Revoke the current refresh token.

**Request Body:**
```json
{
  "refresh_token": "your_refresh_token"
}
```

**Response (200 OK):**
```json
{
  "message": "Successfully logged out"
}
```

---

### Verify Email

**POST** `/auth/verify-email`

Verify email with a 6-digit code.

**Request Body:**
```json
{
  "email": "student@example.com",
  "code": "123456"
}
```

---

### Resend Verification

**POST** `/auth/resend-verification`

Resend a verification code to the given email.

**Request Body:**
```json
{
  "email": "student@example.com"
}
```

---

### Request Password Reset

**POST** `/auth/request-password-reset`

Request a password reset token.

**Request Body:**
```json
{
  "email": "student@example.com"
}
```

---

### Reset Password

**POST** `/auth/reset-password`

Reset password using the token received via email.

**Request Body:**
```json
{
  "token": "reset_token",
  "new_password": "NewSecurePass123"
}
```

---

### Change Password

**POST** `/auth/change-password` 🔒

Change the authenticated user's password.

**Request Body:**
```json
{
  "current_password": "OldPass123",
  "new_password": "NewPass456"
}
```

---

### Get Current User

**GET** `/auth/me` 🔒

Returns the currently authenticated user's profile (same shape as register response).

---

### Check Verification Status

**GET** `/auth/me/verified` 🔒

Returns whether the current user is verified.

---

## Users Endpoints

Prefix: `/users`

### Get Profile

**GET** `/users/me` 🔒

Returns the authenticated user's profile.

---

### Update Profile

**PUT** `/users/me` 🔒

**Request Body** (all fields optional):
```json
{
  "full_name": "Jane Doe",
  "student_type": "graduate",
  "age": 25
}
```

**Response:** Updated `UserResponse`.

---

### Delete Account

**DELETE** `/users/me` 🔒

Permanently deletes the authenticated user's account and all associated data.

**Response:** `204 No Content`

---

## Subjects Endpoints 🔒✅

Prefix: `/subjects`

### Create Subject

**POST** `/subjects`

**Request Body:**
```json
{
  "name": "Mathematics",
  "color": "#ef4444",
  "icon": "📐",
  "description": "Calculus and Linear Algebra"
}
```

| Field | Type | Required | Default |
|-------|------|----------|---------|
| name | string | yes | — |
| color | string | no | `#0ea5e9` |
| icon | string | no | `📚` |
| description | string | no | null |

**Response (201 Created):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "name": "Mathematics",
  "color": "#ef4444",
  "icon": "📐",
  "description": "Calculus and Linear Algebra",
  "is_archived": false,
  "created_at": "2026-02-27T10:00:00",
  "updated_at": "2026-02-27T10:00:00"
}
```

---

### List Subjects

**GET** `/subjects`

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| include_archived | bool | false | Include archived subjects |
| skip | int | 0 | Offset for pagination |
| limit | int | 100 | Max results (1–100) |

**Response:** Array of `SubjectResponse`.

---

### Get Subject

**GET** `/subjects/{subject_id}`

---

### Update Subject

**PUT** `/subjects/{subject_id}`

**Request Body** (all fields optional):
```json
{
  "name": "Math 201",
  "color": "#22c55e"
}
```

---

### Delete Subject

**DELETE** `/subjects/{subject_id}`

**Response:** `204 No Content`

---

### Archive Subject

**POST** `/subjects/{subject_id}/archive`

---

### Unarchive Subject

**POST** `/subjects/{subject_id}/unarchive`

---

## Study Sessions Endpoints 🔒✅

Prefix: `/sessions`

### Create Session

**POST** `/sessions`

**Request Body:**
```json
{
  "subject_id": "uuid",
  "session_type": "focused_study",
  "planned_duration_minutes": 90,
  "notes": "Focus on chapter 5"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| subject_id | string | yes | UUID of the subject |
| session_type | string | yes | `focused_study`, `practice`, `reading`, or `review` |
| planned_duration_minutes | int | no | Planned duration |
| notes | string | no | Session notes |

**Response (201 Created):** `StudySessionResponse`

```json
{
  "id": "uuid",
  "user_id": "uuid",
  "subject_id": "uuid",
  "session_type": "focused_study",
  "status": "active",
  "start_time": "2026-02-27T10:00:00",
  "end_time": null,
  "planned_duration_minutes": 90,
  "actual_duration_minutes": null,
  "pause_count": 0,
  "total_pause_duration_minutes": 0,
  "productivity_score": null,
  "focus_score": null,
  "energy_level": null,
  "difficulty_level": null,
  "satisfaction_level": null,
  "notes": "Focus on chapter 5",
  "created_at": "2026-02-27T10:00:00",
  "updated_at": "2026-02-27T10:00:00"
}
```

---

### List Sessions

**GET** `/sessions`

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| subject_id | string | null | Filter by subject |
| status | string | null | `active`, `paused`, `completed`, `cancelled` |
| start_date | datetime | null | Filter from date |
| end_date | datetime | null | Filter to date |
| skip | int | 0 | Offset |
| limit | int | 100 | Max results (1–100) |

**Response:** Array of `StudySessionResponse`.

---

### Get Session

**GET** `/sessions/{session_id}`

---

### Update Session

**PUT** `/sessions/{session_id}`

**Request Body** (all fields optional):
```json
{
  "notes": "Updated notes",
  "planned_duration_minutes": 60
}
```

---

### Delete Session

**DELETE** `/sessions/{session_id}`

**Response:** `204 No Content`

---

### Start Session

**POST** `/sessions/{session_id}/start`

Sets the session to active and records the start time.

---

### Pause Session

**POST** `/sessions/{session_id}/pause`

Pauses an active session. Increments `pause_count`.

---

### Resume Session

**POST** `/sessions/{session_id}/resume`

Resumes a paused session.

---

### Complete Session

**POST** `/sessions/{session_id}/complete`

Complete a session with feedback.

**Request Body:**
```json
{
  "productivity_score": 85,
  "focus_score": 88,
  "energy_level": 4,
  "difficulty_level": 3,
  "satisfaction_level": 5,
  "notes": "Great session"
}
```

| Field | Type | Required | Range |
|-------|------|----------|-------|
| productivity_score | int | no | 0–100 |
| focus_score | int | no | 0–100 |
| energy_level | int | no | 1–5 |
| difficulty_level | int | no | 1–5 |
| satisfaction_level | int | no | 1–5 |
| notes | string | no | — |

---

## Goals Endpoints 🔒✅

Prefix: `/goals`

### Create Goal

**POST** `/goals`

**Request Body:**
```json
{
  "goal_type": "weekly",
  "target_hours": 20,
  "subject_id": null,
  "start_date": "2026-03-01",
  "end_date": "2026-03-07"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| goal_type | string | yes | `daily`, `weekly`, or `monthly` |
| target_hours | int | yes | Target study hours |
| subject_id | string | no | Optional subject filter |
| start_date | date | yes | Period start |
| end_date | date | yes | Period end |

**Response (201 Created):** `GoalResponse`

```json
{
  "id": "uuid",
  "user_id": "uuid",
  "subject_id": null,
  "goal_type": "weekly",
  "target_hours": 20,
  "start_date": "2026-03-01",
  "end_date": "2026-03-07",
  "current_hours": 0.0,
  "is_achieved": false,
  "achieved_at": null,
  "created_at": "2026-02-27T10:00:00",
  "updated_at": "2026-02-27T10:00:00"
}
```

---

### List Goals

**GET** `/goals`

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| subject_id | string | null | Filter by subject |
| is_achieved | bool | null | Filter by achieved status |
| skip | int | 0 | Offset |
| limit | int | 100 | Max results (1–100) |

---

### Get Goal

**GET** `/goals/{goal_id}`

---

### Update Goal

**PUT** `/goals/{goal_id}`

---

### Delete Goal

**DELETE** `/goals/{goal_id}`

**Response:** `204 No Content`

---

### Update Goal Progress

**POST** `/goals/{goal_id}/progress`

**Request Body:**
```json
{
  "progress": 12.5
}
```

---

### Mark Goal Achieved

**POST** `/goals/{goal_id}/achieve`

---

## Deadlines Endpoints 🔒✅

Prefix: `/deadlines`

### Create Deadline

**POST** `/deadlines`

**Request Body:**
```json
{
  "subject_id": "uuid",
  "title": "Calculus Midterm",
  "description": "Chapters 1-5",
  "deadline_date": "2026-03-15T09:00:00",
  "priority": "high"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| subject_id | string | yes | Related subject |
| title | string | yes | Deadline title |
| description | string | no | Details |
| deadline_date | datetime | yes | Due date/time |
| priority | string | no | `low`, `medium` (default), `high`, `urgent` |

**Response (201 Created):** `DeadlineResponse`

```json
{
  "id": "uuid",
  "user_id": "uuid",
  "subject_id": "uuid",
  "title": "Calculus Midterm",
  "description": "Chapters 1-5",
  "deadline_date": "2026-03-15T09:00:00",
  "priority": "high",
  "is_completed": false,
  "completed_at": null,
  "created_at": "2026-02-27T10:00:00",
  "updated_at": "2026-02-27T10:00:00"
}
```

---

### List Deadlines

**GET** `/deadlines`

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| subject_id | string | null | Filter by subject |
| is_completed | bool | null | Filter by completion |
| priority | string | null | Filter by priority |
| skip | int | 0 | Offset |
| limit | int | 100 | Max results (1–100) |

---

### Get Deadline

**GET** `/deadlines/{deadline_id}`

---

### Update Deadline

**PUT** `/deadlines/{deadline_id}`

---

### Delete Deadline

**DELETE** `/deadlines/{deadline_id}`

**Response:** `204 No Content`

---

### Mark Complete

**POST** `/deadlines/{deadline_id}/complete`

---

### Mark Incomplete

**POST** `/deadlines/{deadline_id}/incomplete`

---

## Wellness Endpoints 🔒✅

Prefix: `/wellness`

### Log Wellness

**POST** `/wellness`

**Request Body:**
```json
{
  "date": "2026-02-27",
  "sleep_hours": 7.5,
  "sleep_quality": 4,
  "energy_level": 4,
  "stress_level": 3,
  "mood": 4,
  "focus_score": 75,
  "notes": "Feeling good today"
}
```

| Field | Type | Required | Range |
|-------|------|----------|-------|
| date | date | yes | — |
| sleep_hours | float | no | 0–24 |
| sleep_quality | int | no | 1–5 |
| energy_level | int | no | 1–5 |
| stress_level | int | no | 1–10 |
| mood | int | no | 1–5 |
| focus_score | int | no | 1–100 |
| notes | string | no | — |

**Response (201 Created):** `DailyWellnessResponse`

```json
{
  "id": "uuid",
  "user_id": "uuid",
  "date": "2026-02-27",
  "sleep_hours": 7.5,
  "sleep_quality": 4,
  "energy_level": 4,
  "stress_level": 3,
  "mood": 4,
  "focus_score": 75,
  "notes": "Feeling good today",
  "created_at": "2026-02-27T10:00:00",
  "updated_at": "2026-02-27T10:00:00"
}
```

---

### List Wellness Entries

**GET** `/wellness`

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| start_date | date | null | Filter from date |
| end_date | date | null | Filter to date |
| skip | int | 0 | Offset |
| limit | int | 100 | Max results (1–100) |

---

### Get Wellness by Date

**GET** `/wellness/date/{wellness_date}`

Returns the wellness entry for a specific date (format: `YYYY-MM-DD`).

---

### Get Wellness by ID

**GET** `/wellness/{wellness_id}`

---

### Update Wellness

**PUT** `/wellness/{wellness_id}`

---

### Delete Wellness

**DELETE** `/wellness/{wellness_id}`

**Response:** `204 No Content`

---

## Analytics Endpoints 🔒✅

Prefix: `/analytics`

### Dashboard Analytics

**GET** `/analytics/dashboard`

Comprehensive dashboard data.

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| days | int | 30 | Analysis period (1–365) |

**Response (200 OK):** `DashboardAnalytics`
```json
{
  "study_time": { ... },
  "subject_stats": [ ... ],
  "productivity_trends": [ ... ],
  "goal_progress": [ ... ],
  "streak_info": { ... },
  "wellness_correlation": { ... }
}
```

---

### Study Time Stats

**GET** `/analytics/study-time`

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| start_date | date | 30 days ago | Start of analysis |
| end_date | date | today | End of analysis |
| subject_id | UUID | null | Filter by subject |

**Response:** `StudyTimeStats`
```json
{
  "total_minutes": 1200,
  "total_sessions": 15,
  "average_session_minutes": 80.0,
  "average_productivity": 82.5,
  "daily_average_minutes": 40.0,
  "most_productive_day": "Wednesday",
  "most_active_hour": 14
}
```

---

### Subject Stats

**GET** `/analytics/subjects`

**Query Parameters:**

| Param | Type | Default |
|-------|------|---------|
| start_date | date | 30 days ago |
| end_date | date | today |

**Response:** Array of `SubjectStats`
```json
[
  {
    "subject_id": "uuid",
    "subject_name": "Mathematics",
    "total_minutes": 450,
    "session_count": 8,
    "average_productivity": 85.0,
    "percentage_of_total": 35.5
  }
]
```

---

### Productivity Trends

**GET** `/analytics/productivity-trends`

**Query Parameters:**

| Param | Type | Default |
|-------|------|---------|
| days | int | 30 (1–365) |

**Response:** Array of `ProductivityTrend`
```json
[
  {
    "date": "2026-02-27",
    "average_productivity": 85.0,
    "total_minutes": 120,
    "session_count": 2
  }
]
```

---

### Goal Progress

**GET** `/analytics/goals/progress`

**Query Parameters:**

| Param | Type | Default |
|-------|------|---------|
| subject_id | UUID | null |

**Response:** Array of `GoalProgress`
```json
[
  {
    "goal_id": "uuid",
    "goal_type": "weekly",
    "target_hours": 20,
    "current_hours": 12.5,
    "progress_percentage": 62.5,
    "days_remaining": 3,
    "is_on_track": true
  }
]
```

---

### Streak Info

**GET** `/analytics/streak`

**Response:** `StreakInfo`
```json
{
  "current_streak": 7,
  "longest_streak": 21,
  "last_study_date": "2026-02-27",
  "is_active_today": true
}
```

---

### Wellness Correlation

**GET** `/analytics/wellness-correlation`

**Query Parameters:**

| Param | Type | Default |
|-------|------|---------|
| days | int | 30 (7–365) |

**Response:** `WellnessCorrelation`
```json
{
  "sleep_productivity_correlation": 0.72,
  "stress_productivity_correlation": -0.45,
  "energy_productivity_correlation": 0.65,
  "average_sleep_hours": 7.2,
  "average_stress_level": 4.5,
  "average_energy_level": 3.8,
  "insight": "Better sleep correlates with higher productivity for you."
}
```

---

## AI Endpoints 🔒

Prefix: `/ai`

### Predict Productivity

**POST** `/ai/predict-productivity`

Predict productivity score based on current habits using the ML model.

**Request Body:**
```json
{
  "study_hours_per_day": 5.0,
  "sleep_hours": 7.5,
  "stress_level": 4,
  "focus_score": 70
}
```

| Field | Type | Required | Range |
|-------|------|----------|-------|
| study_hours_per_day | float | yes | 0–24 |
| sleep_hours | float | yes | 0–24 |
| stress_level | int | yes | 1–10 |
| focus_score | int | yes | 1–100 |

**Response (200 OK):** `AiProductivityPrediction`
```json
{
  "predicted_score": 78.5,
  "confidence": 0.87,
  "top_factors": [
    {"factor": "Study Hours", "impact": "positive", "value": 5.0},
    {"factor": "Focus", "impact": "positive", "value": 70.0},
    {"factor": "Sleep", "impact": "positive", "value": 7.5},
    {"factor": "Stress", "impact": "positive", "value": 4.0}
  ],
  "recommendation": "Great job! Your habits are well-balanced for high productivity."
}
```

**Error (503):** Model not trained yet.

---

### Peak Study Hours

**GET** `/ai/peak-hours`

Analyze the user's completed sessions to find peak productivity hours.

**Response (200 OK):** `PeakStudyHoursResponse`
```json
{
  "peak_hours": [
    {"hour": 9, "average_productivity": 85.0, "session_count": 5},
    {"hour": 14, "average_productivity": 82.0, "session_count": 8},
    {"hour": 20, "average_productivity": 70.0, "session_count": 3}
  ],
  "best_hour": 9,
  "best_productivity": 85.0,
  "total_sessions_analyzed": 16
}
```

**Error (404):** Fewer than 3 completed sessions with productivity scores.

---

## Error Responses

All errors follow FastAPI's standard format:

```json
{
  "detail": "Error message description"
}
```

**Common Status Codes:**

| Code | Meaning |
|------|---------|
| 400 | Bad Request |
| 401 | Unauthorized (missing/invalid token) |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Validation Error (check `detail` array for field errors) |
| 500 | Internal Server Error |
| 503 | Service Unavailable (e.g., ML model not loaded) |

---

## Interactive Docs

FastAPI provides auto-generated interactive documentation:

- **Swagger UI:** `http://localhost:5000/docs`
- **ReDoc:** `http://localhost:5000/redoc`

---

🔒 = Requires authentication
🔒✅ = Requires authentication + email verification
