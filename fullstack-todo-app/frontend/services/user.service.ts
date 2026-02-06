/**
 * User API service.
 */

import { api } from "./api";
import type { APIResponse } from "@/types/api";
import type { User, UserUpdate } from "@/types/user";

export const userService = {
  /**
   * Get current user's profile.
   */
  async getProfile(): Promise<APIResponse<User>> {
    const response = await api.get<APIResponse<User>>("/users/me");
    return response.data;
  },

  /**
   * Update current user's profile.
   */
  async updateProfile(data: UserUpdate): Promise<APIResponse<User>> {
    const response = await api.patch<APIResponse<User>>("/users/me", data);
    return response.data;
  },
};
