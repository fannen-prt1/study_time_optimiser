import apiClient, { handleApiError } from './apiClient';
import { ENDPOINTS } from '../config/constants';
import type {
  DashboardAnalytics,
  StudyTimeStats,
  SubjectStats,
  ProductivityTrend,
  StreakInfo,
  WellnessCorrelation,
} from '../types';

export const analyticsService = {
  // Get full dashboard analytics
  async getDashboard(days = 30): Promise<DashboardAnalytics> {
    try {
      const response = await apiClient.get<DashboardAnalytics>(ENDPOINTS.ANALYTICS.DASHBOARD, {
        params: { days },
      });
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Get study time stats
  async getStudyTime(days = 30): Promise<StudyTimeStats> {
    try {
      const response = await apiClient.get<StudyTimeStats>(ENDPOINTS.ANALYTICS.STUDY_TIME, {
        params: { days },
      });
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Get subject stats
  async getSubjectStats(days = 30): Promise<SubjectStats[]> {
    try {
      const response = await apiClient.get<SubjectStats[]>(ENDPOINTS.ANALYTICS.SUBJECTS, {
        params: { days },
      });
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Get productivity trends
  async getProductivityTrends(days = 30): Promise<ProductivityTrend[]> {
    try {
      const response = await apiClient.get<ProductivityTrend[]>(
        ENDPOINTS.ANALYTICS.PRODUCTIVITY_TRENDS,
        { params: { days } }
      );
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Get streak info
  async getStreak(): Promise<StreakInfo> {
    try {
      const response = await apiClient.get<StreakInfo>(ENDPOINTS.ANALYTICS.STREAK);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Get wellness correlation
  async getWellnessCorrelation(days = 30): Promise<WellnessCorrelation> {
    try {
      const response = await apiClient.get<WellnessCorrelation>(
        ENDPOINTS.ANALYTICS.WELLNESS_CORRELATION,
        { params: { days } }
      );
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },
};
