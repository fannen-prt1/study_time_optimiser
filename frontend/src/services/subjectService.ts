import apiClient, { handleApiError } from './apiClient';
import { ENDPOINTS } from '../config/constants';
import type { Subject, CreateSubjectRequest } from '../types';

export const subjectService = {
  // Get all subjects
  async getAll(includeArchived = false): Promise<Subject[]> {
    try {
      const response = await apiClient.get<Subject[]>(ENDPOINTS.SUBJECTS.BASE, {
        params: { include_archived: includeArchived },
      });
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Get subject by ID
  async getById(id: string): Promise<Subject> {
    try {
      const response = await apiClient.get<Subject>(ENDPOINTS.SUBJECTS.BY_ID(id));
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Create subject
  async create(data: CreateSubjectRequest): Promise<Subject> {
    try {
      const response = await apiClient.post<Subject>(ENDPOINTS.SUBJECTS.BASE, data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Update subject
  async update(id: string, data: Partial<CreateSubjectRequest>): Promise<Subject> {
    try {
      const response = await apiClient.put<Subject>(ENDPOINTS.SUBJECTS.BY_ID(id), data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Delete subject
  async delete(id: string): Promise<void> {
    try {
      await apiClient.delete(ENDPOINTS.SUBJECTS.BY_ID(id));
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Archive subject
  async archive(id: string): Promise<Subject> {
    try {
      const response = await apiClient.post<Subject>(ENDPOINTS.SUBJECTS.ARCHIVE(id));
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Unarchive subject
  async unarchive(id: string): Promise<Subject> {
    try {
      const response = await apiClient.post<Subject>(ENDPOINTS.SUBJECTS.UNARCHIVE(id));
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },
};
