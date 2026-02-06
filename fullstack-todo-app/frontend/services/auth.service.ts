/**
 * Authentication API service.
 */

import { api } from "./api";
import type { APIResponse, TokenData } from "@/types/api";
import type { UserCreate, LoginRequest } from "@/types/user";

export const authService = {
  /**
   * Register a new user.
   */
  async signup(data: UserCreate): Promise<APIResponse<TokenData>> {
    const response = await api.post<APIResponse<TokenData>>("/auth/signup", data);
    return response.data;
  },

  /**
   * Login with email and password.
   */
  async login(data: LoginRequest): Promise<APIResponse<TokenData>> {
    const response = await api.post<APIResponse<TokenData>>("/auth/login", data);
    return response.data;
  },

  /**
   * Refresh access token using refresh token cookie.
   */
  async refreshToken(): Promise<APIResponse<TokenData>> {
    const response = await api.post<APIResponse<TokenData>>("/auth/refresh");
    return response.data;
  },

  /**
   * Logout - clears refresh token cookie.
   */
  async logout(): Promise<APIResponse<null>> {
    const response = await api.post<APIResponse<null>>("/auth/logout");
    return response.data;
  },
};
