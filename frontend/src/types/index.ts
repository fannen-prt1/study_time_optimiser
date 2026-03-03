// User Types
export interface User {
  id: string;
  email: string;
  full_name: string;
  age: number;
  student_type: 'high_school' | 'college' | 'graduate' | 'professional';
  profile_image_url?: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
  last_login?: string;
}

// Auth Types
export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  full_name: string;
  age: number;
  student_type: 'high_school' | 'college' | 'graduate' | 'professional';
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface ChangePasswordRequest {
  current_password: string;
  new_password: string;
}

// Subject Types
export interface Subject {
  id: string;
  user_id: string;
  name: string;
  color: string;
  icon?: string;
  description?: string;
  is_archived: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateSubjectRequest {
  name: string;
  color: string;
  icon?: string;
  description?: string;
}

// Study Session Types
export type SessionType = 'focused_study' | 'practice' | 'reading' | 'review';
export type SessionStatus = 'active' | 'paused' | 'completed' | 'cancelled';

export interface StudySession {
  id: string;
  user_id: string;
  subject_id: string;
  session_type: SessionType;
  planned_duration_minutes?: number;
  actual_duration_minutes?: number;
  start_time: string;
  end_time?: string;
  status: SessionStatus;
  pause_count: number;
  total_pause_duration_minutes: number;
  notes?: string;
  productivity_score?: number;
  focus_score?: number;
  energy_level?: number;
  difficulty_level?: number;
  satisfaction_level?: number;
  created_at: string;
  updated_at: string;
}

export interface CreateSessionRequest {
  subject_id: string;
  session_type: SessionType;
  planned_duration_minutes?: number;
  start_time?: string;
  notes?: string;
}

export interface CompleteSessionRequest {
  productivity_score?: number;
  focus_score?: number;
  energy_level?: number;
  difficulty_level?: number;
  satisfaction_level?: number;
  notes?: string;
}

// Goal Types
export type GoalType = 'daily' | 'weekly' | 'monthly';

export interface Goal {
  id: string;
  user_id: string;
  subject_id?: string;
  goal_type: GoalType;
  target_hours: number;
  start_date: string;
  end_date: string;
  current_hours: number;
  is_achieved: boolean;
  achieved_at?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateGoalRequest {
  subject_id?: string;
  goal_type: GoalType;
  target_hours: number;
  start_date?: string;
}

// Deadline Types
export type Priority = 'low' | 'medium' | 'high' | 'urgent';

export interface Deadline {
  id: string;
  user_id: string;
  subject_id: string;
  title: string;
  description?: string;
  deadline_date: string;
  priority: Priority;
  is_completed: boolean;
  completed_at?: string;
  reminder_sent: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateDeadlineRequest {
  subject_id: string;
  title: string;
  description?: string;
  deadline_date: string;
  priority: Priority;
}

// Wellness Types
export interface DailyWellness {
  id: string;
  user_id: string;
  date: string;
  sleep_hours?: number;
  sleep_quality?: number;
  energy_level?: number;
  stress_level?: number;
  mood?: number;
  focus_score?: number;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateWellnessRequest {
  date: string;
  sleep_hours?: number;
  sleep_quality?: number;
  energy_level?: number;
  stress_level?: number;
  mood?: number;
  focus_score?: number;
  notes?: string;
}

// Analytics Types
export interface StudyTimeStats {
  total_minutes: number;
  total_sessions: number;
  average_session_minutes: number;
  total_planned_minutes: number;
  completion_rate: number;
  average_productivity_score: number;
  average_focus_score: number;
}

export interface SubjectStats {
  subject_id: string;
  subject_name: string;
  subject_color: string;
  subject_icon?: string;
  total_sessions: number;
  total_minutes: number;
  average_productivity: number;
}

export interface ProductivityTrend {
  date: string;
  total_minutes: number;
  session_count: number;
  average_productivity: number;
  average_focus: number;
}

export interface GoalProgress {
  goal_id: string;
  title: string;
  subject_name: string;
  goal_type: string;
  current_value: number;
  target_value: number;
  progress_percentage: number;
  is_achieved: boolean;
  days_remaining?: number;
  target_date?: string;
}

export interface StreakInfo {
  current_streak: number;
  longest_streak: number;
  total_study_days: number;
  last_study_date?: string;
}

export interface WellnessCorrelation {
  average_sleep_hours: number;
  average_productivity: number;
  high_productivity_sleep_average: number;
  low_productivity_sleep_average: number;
  optimal_sleep_range: [number, number];
  energy_productivity_correlation: string;
}

export interface DashboardAnalytics {
  study_time_stats: StudyTimeStats;
  subject_stats: SubjectStats[];
  productivity_trends: ProductivityTrend[];
  goal_progress: GoalProgress[];
  streak_info: StreakInfo;
  wellness_correlation: WellnessCorrelation;
  upcoming_deadlines: Deadline[];
}

// AI Prediction Types
export interface AiProductivityPrediction {
  predicted_score: number;
  confidence: number;
  top_factors: { factor: string; impact: string; value: number }[];
  recommendation: string;
}

export interface PeakStudyHour {
  hour: number;
  average_productivity: number;
  session_count: number;
}

export interface PeakStudyHoursResponse {
  peak_hours: PeakStudyHour[];
  best_hour: number;
  best_productivity: number;
  total_sessions_analyzed: number;
}

export interface AiPredictionInput {
  study_hours_per_day: number;
  sleep_hours: number;
  stress_level: number;
  focus_score: number;
}


