/**
 * User types matching backend schema.
 */

export interface User {
  id: string;
  email: string;
  username: string;
  created_at: string;
}

export interface UserCreate {
  email: string;
  username: string;
  password: string;
}

export interface UserUpdate {
  username?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}
