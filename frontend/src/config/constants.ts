// API Configuration
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api/v1';

// Storage Keys
export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'access_token',
  REFRESH_TOKEN: 'refresh_token',
  USER: 'user',
} as const;

// API Endpoints
export const ENDPOINTS = {
  // Auth
  AUTH: {
    REGISTER: '/auth/register',
    LOGIN: '/auth/login',
    LOGOUT: '/auth/logout',
    REFRESH: '/auth/refresh',
    ME: '/auth/me',
    CHANGE_PASSWORD: '/auth/change-password',
    VERIFY_EMAIL: '/auth/verify-email',
    RESEND_VERIFICATION: '/auth/resend-verification',
    FORGOT_PASSWORD: '/auth/forgot-password',
    RESET_PASSWORD: '/auth/reset-password',
  },
  // Users
  USERS: {
    ME: '/users/me',
  },
  // Subjects
  SUBJECTS: {
    BASE: '/subjects/',
    BY_ID: (id: string) => `/subjects/${id}`,
    ARCHIVE: (id: string) => `/subjects/${id}/archive`,
    UNARCHIVE: (id: string) => `/subjects/${id}/unarchive`,
  },
  // Study Sessions
  SESSIONS: {
    BASE: '/sessions/',
    BY_ID: (id: string) => `/sessions/${id}`,
    START: (id: string) => `/sessions/${id}/start`,
    PAUSE: (id: string) => `/sessions/${id}/pause`,
    RESUME: (id: string) => `/sessions/${id}/resume`,
    COMPLETE: (id: string) => `/sessions/${id}/complete`,
  },
  // Goals
  GOALS: {
    BASE: '/goals/',
    BY_ID: (id: string) => `/goals/${id}`,
    PROGRESS: (id: string) => `/goals/${id}/progress`,
    ACHIEVE: (id: string) => `/goals/${id}/achieve`,
  },
  // Deadlines
  DEADLINES: {
    BASE: '/deadlines/',
    BY_ID: (id: string) => `/deadlines/${id}`,
    COMPLETE: (id: string) => `/deadlines/${id}/complete`,
    INCOMPLETE: (id: string) => `/deadlines/${id}/incomplete`,
  },
  // Wellness
  WELLNESS: {
    BASE: '/wellness/',
    BY_ID: (id: string) => `/wellness/${id}`,
    BY_DATE: (date: string) => `/wellness/date/${date}`,
  },
  // Analytics
  ANALYTICS: {
    DASHBOARD: '/analytics/dashboard',
    STUDY_TIME: '/analytics/study-time',
    SUBJECTS: '/analytics/subjects',
    PRODUCTIVITY_TRENDS: '/analytics/productivity-trends',
    GOAL_PROGRESS: '/analytics/goals/progress',
    STREAK: '/analytics/streak',
    WELLNESS_CORRELATION: '/analytics/wellness-correlation',
  },
  // AI
  AI: {
    PREDICT_PRODUCTIVITY: '/ai/predict-productivity',
    PEAK_HOURS: '/ai/peak-hours',
  },
} as const;


