import apiClient, { handleApiError } from './apiClient';
import { ENDPOINTS, STORAGE_KEYS } from '../config/constants';
import type {
  LoginRequest,
  RegisterRequest,
  AuthResponse,
  User,
  ChangePasswordRequest,
} from '../types';

export interface RegisterResponse extends User {
  message?: string;
  _dev_verification_token?: string;
  _dev_verify_url?: string;
}

export const authService = {
  // Register new user
  async register(data: RegisterRequest): Promise<RegisterResponse> {
    try {
      const response = await apiClient.post<RegisterResponse>(ENDPOINTS.AUTH.REGISTER, data);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Login
  async login(data: LoginRequest): Promise<AuthResponse> {
    try {
      const response = await apiClient.post<AuthResponse>(ENDPOINTS.AUTH.LOGIN, data);
      
      // Store tokens
      localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, response.data.access_token);
      localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, response.data.refresh_token);
      
      // Fetch and store user data
      const user = await this.getCurrentUser();
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user));
      
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Logout
  async logout(): Promise<void> {
    try {
      const refreshToken = localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);
      if (refreshToken) {
        await apiClient.post(ENDPOINTS.AUTH.LOGOUT, { refresh_token: refreshToken });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Clear local storage regardless of API call result
      localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN);
      localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN);
      localStorage.removeItem(STORAGE_KEYS.USER);
    }
  },

  // Get current user
  async getCurrentUser(): Promise<User> {
    try {
      const response = await apiClient.get<User>(ENDPOINTS.AUTH.ME);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  // Change password
  async changePassword(data: ChangePasswordRequest): Promise<void> {
    try {
      await apiClient.post(ENDPOINTS.AUTH.CHANGE_PASSWORD, data);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },



  // Check if user is authenticated
  isAuthenticated(): boolean {
    return !!localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);
  },

  // Get stored user
  getStoredUser(): User | null {
    const userStr = localStorage.getItem(STORAGE_KEYS.USER);
    if (!userStr) return null;
    try {
      return JSON.parse(userStr);
    } catch {
      return null;
    }
  },
};
