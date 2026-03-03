import apiClient, { handleApiError } from './apiClient';
import { ENDPOINTS } from '../config/constants';
import type { StudySession, CreateSessionRequest, CompleteSessionRequest } from '../types';

export const sessionService = {
  // Get all sessions
  async getAll(params?: {
    subject_id?: string;
    status?: string;
    skip?: number;
    limit?: number;
  }): Promise<StudySession[]> {
    try {
      const response = await apiClient.get<StudySession[]>(ENDPOINTS.SESSIONS.BASE, { params });
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Get session by ID
  async getById(id: string): Promise<StudySession> {
    try {
      const response = await apiClient.get<StudySession>(ENDPOINTS.SESSIONS.BY_ID(id));
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Create session
  async create(data: CreateSessionRequest): Promise<StudySession> {
    try {
      const response = await apiClient.post<StudySession>(ENDPOINTS.SESSIONS.BASE, data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Start session
  async start(id: string): Promise<StudySession> {
    try {
      const response = await apiClient.post<StudySession>(ENDPOINTS.SESSIONS.START(id));
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Pause session
  async pause(id: string): Promise<StudySession> {
    try {
      const response = await apiClient.post<StudySession>(ENDPOINTS.SESSIONS.PAUSE(id));
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Resume session
  async resume(id: string): Promise<StudySession> {
    try {
      const response = await apiClient.post<StudySession>(ENDPOINTS.SESSIONS.RESUME(id));
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Complete session
  async complete(id: string, data: CompleteSessionRequest): Promise<StudySession> {
    try {
      const response = await apiClient.post<StudySession>(
        ENDPOINTS.SESSIONS.COMPLETE(id),
        data
      );
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Delete session
  async delete(id: string): Promise<void> {
    try {
      await apiClient.delete(ENDPOINTS.SESSIONS.BY_ID(id));
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },
};
