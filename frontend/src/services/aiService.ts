import apiClient, { handleApiError } from './apiClient';
import { ENDPOINTS } from '../config/constants';
import type {
  AiProductivityPrediction,
  AiPredictionInput,
  PeakStudyHoursResponse,
} from '../types';

export const aiService = {
  // Predict productivity score based on current inputs
  async predictProductivity(input: AiPredictionInput): Promise<AiProductivityPrediction> {
    try {
      const response = await apiClient.post<AiProductivityPrediction>(
        ENDPOINTS.AI.PREDICT_PRODUCTIVITY,
        input
      );
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Get user's peak study hours from session history
  async getPeakHours(): Promise<PeakStudyHoursResponse> {
    try {
      const response = await apiClient.get<PeakStudyHoursResponse>(ENDPOINTS.AI.PEAK_HOURS);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },
};
