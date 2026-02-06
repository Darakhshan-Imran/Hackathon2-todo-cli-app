/**
 * API response types matching backend schema.
 */

export interface APIResponse<T> {
  success: boolean;
  data: T | null;
  error: string | null;
  timestamp: string;
}

export interface PaginatedData<T> {
  items: T[];
  page: number;
  per_page: number;
  total: number;
  total_pages: number;
}

export interface TokenData {
  access_token: string;
  token_type: string;
}
