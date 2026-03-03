# Study Time Optimizer — User Guide

Welcome to **Study Time Optimizer**! This guide covers all the features available in the application.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Dashboard](#dashboard)
3. [Subjects](#subjects)
4. [Study Sessions](#study-sessions)
5. [Deadlines](#deadlines)
6. [Wellness Tracking](#wellness-tracking)
7. [Analytics](#analytics)
8. [AI Productivity Prediction](#ai-productivity-prediction)
9. [Account Management](#account-management)
10. [Tips for Success](#tips-for-success)

---

## Getting Started

### Creating Your Account

1. Navigate to the app and click **Register**
2. Fill in your details:
   - **Email address**
   - **Password** (minimum 8 characters, must include uppercase, lowercase, and a digit)
   - **Full name**
   - **Student type** — High School, College, Graduate, or Professional
   - **Age** (optional)
3. Click **Create Account**
4. Verify your email with the 6-digit code sent to your inbox

### Logging In

1. Enter your email and password on the **Login** page
2. You'll receive an access token and refresh token automatically
3. The app keeps you logged in and refreshes your session as needed

---

## Dashboard

The dashboard is your home page showing an overview of your study activity.

### What You'll See

- **Study time statistics** — total minutes, sessions, averages
- **Subject breakdown** — time spent per subject
- **Productivity trends** — daily productivity scores over time
- **Goal progress** — how close you are to your study targets
- **Streak info** — current and longest consecutive study day streaks
- **Wellness correlation** — how sleep, stress, and energy relate to your productivity

---

## Subjects

Subjects represent the courses or topics you study.

### Adding a Subject

1. Go to **Subjects** from the sidebar
2. Click **Add Subject**
3. Fill in:
   - **Name** — e.g., "Mathematics"
   - **Color** — hex color for visual identification (default: sky blue)
   - **Icon** — emoji icon (default: 📚)
   - **Description** (optional)
4. Save

### Managing Subjects

- **Edit** — update name, color, icon, or description
- **Archive** — hide a subject without deleting it (use Unarchive to restore)
- **Delete** — permanently remove a subject and all its sessions

---

## Study Sessions

Study sessions are the core of the app — they track when and how you study.

### Creating a Session

1. Go to **Sessions**
2. Click **New Session**
3. Choose:
   - **Subject** — select from your subjects
   - **Session Type**:
     - 📖 **Focused Study** — deep learning and understanding
     - ✏️ **Practice** — exercises and problem-solving
     - 📚 **Reading** — textbook or article reading
     - 🔄 **Review** — revision of learned material
   - **Planned Duration** (optional) — how long you plan to study
   - **Notes** (optional)

### Session Lifecycle

Sessions go through these statuses:

| Status | Description |
|--------|-------------|
| **Active** | Session is in progress |
| **Paused** | Session is temporarily paused |
| **Completed** | Session finished with feedback |
| **Cancelled** | Session was abandoned |

### Session Controls

- **Start** — begin the session
- **Pause** — take a break (pause count is tracked)
- **Resume** — continue after a pause
- **Complete** — finish and provide feedback

### Providing Feedback

After completing a session, rate:

| Metric | Scale | Description |
|--------|-------|-------------|
| Productivity | 0–100 | How productive was the session? |
| Focus | 0–100 | How well could you concentrate? |
| Energy | 1–5 | Your energy level |
| Difficulty | 1–5 | How challenging was the material? |
| Satisfaction | 1–5 | Overall session satisfaction |
| Notes | text | Any additional comments |

> **Why feedback matters:** The analytics system uses this data to identify patterns and the AI uses it to determine your peak study hours.

---

## Deadlines

Track upcoming exams, assignments, and project due dates.

### Adding a Deadline

1. Go to **Deadlines** from the sidebar
2. Click **Add Deadline**
3. Fill in:
   - **Title** — e.g., "Calculus Midterm"
   - **Subject** — related subject
   - **Date & Time** — when it's due
   - **Priority** — Low, Medium, High, or Urgent
   - **Description** (optional)
4. Save

### Managing Deadlines

- **Mark Complete** — when you've finished the task
- **Mark Incomplete** — revert if needed
- **Edit** — update details
- **Delete** — remove the deadline

---

## Wellness Tracking

Log daily wellness metrics to understand how your lifestyle affects studying.

### Logging Wellness

1. Go to **Wellness** from the sidebar
2. Click **Log Today's Wellness**
3. Fill in (all optional except date):
   - **Sleep Hours** — how long you slept (0–24)
   - **Sleep Quality** — rating (1–5)
   - **Energy Level** — rating (1–5)
   - **Stress Level** — rating (1–10)
   - **Mood** — rating (1–5)
   - **Focus Score** — rating (1–100)
   - **Notes** (optional)
4. Save

> One entry per day. You can update your entry anytime.

### Why Track Wellness?

The analytics dashboard computes correlations between your wellness metrics and study productivity, helping you understand what lifestyle factors help you study best.

---

## Analytics

The analytics page provides deep insights into your study patterns.

### Available Analytics

| View | Description |
|------|-------------|
| **Dashboard Overview** | Combined view of all analytics for a configurable time period (1–365 days) |
| **Study Time Stats** | Total minutes, sessions, averages, most productive day and hour |
| **Subject Stats** | Per-subject breakdown: time, sessions, productivity, percentage of total |
| **Productivity Trends** | Daily productivity averages over time |
| **Goal Progress** | Progress for each active goal with on-track indicator |
| **Streak Info** | Current streak, longest streak, last study date |
| **Wellness Correlation** | How sleep, stress, and energy correlate with your productivity |

---

## AI Productivity Prediction

The app includes an ML-powered feature that predicts your productivity score.

### How It Works

Enter your current metrics:
- **Study hours per day** (0–24)
- **Sleep hours** (0–24)
- **Stress level** (1–10)
- **Focus score** (1–100)

The AI model returns:
- **Predicted productivity score** (0–100)
- **Confidence level**
- **Impact of each factor** (positive or negative)
- **Personalized recommendation** to improve

### Peak Study Hours

The app also analyzes your completed sessions to find your **peak productivity hours** — which times of day you study best. This requires at least 3 completed sessions with productivity scores.

---

## Account Management

### Profile

- **Update profile** — change name, student type, or age via **Users > My Profile**
- **Change password** — from the authentication settings

### Account Deletion

You can permanently delete your account and all data from **Users > Delete Account**. This action is irreversible.

---

## Tips for Success

### Maximize Your Productivity

1. **Study at consistent times** — helps the peak-hours analysis learn your patterns
2. **Provide honest feedback** — accurate scores improve analytics and AI predictions
3. **Take real breaks** — use the pause feature; your brain needs rest
4. **Set realistic goals** — start achievable, then gradually increase
5. **Balance subjects** — rotate between subjects to prevent burnout
6. **Track wellness daily** — understanding sleep/stress/focus patterns is powerful

### Common Mistakes to Avoid

- Setting unrealistic daily hour targets
- Skipping post-session feedback
- Ignoring breaks during long sessions
- Multitasking during study sessions
- Not logging wellness data

---

## Technical Notes

- **Frontend:** React + TypeScript + Vite, running on port 3000
- **Backend:** FastAPI + SQLAlchemy + SQLite, running on port 5000
- **API Docs:** Visit `http://localhost:5000/docs` for interactive Swagger documentation
- **ML Model:** Stacking ensemble (GradientBoosting + RandomForest + Ridge) trained on student productivity data

---

*Last updated: February 2026*
*Version: 1.0.0*
