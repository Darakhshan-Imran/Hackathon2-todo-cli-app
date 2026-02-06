"use client";

/**
 * Authentication context provider.
 */

import {
  createContext,
  useContext,
  useEffect,
  useState,
  useCallback,
  type ReactNode,
} from "react";
import { useRouter } from "next/navigation";
import { authService } from "@/services/auth.service";
import { userService } from "@/services/user.service";
import {
  setAccessToken,
  clearAccessToken,
} from "@/lib/auth";
import { getErrorMessage } from "@/services/api";
import type { User, UserCreate, LoginRequest } from "@/types/user";

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (data: LoginRequest) => Promise<void>;
  signup: (data: UserCreate) => Promise<void>;
  logout: () => Promise<void>;
  clearError: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const isAuthenticated = user !== null;

  // Try to restore session on mount
  useEffect(() => {
    const initAuth = async () => {
      try {
        // Try to refresh token (will use HttpOnly cookie)
        const response = await authService.refreshToken();
        if (response.success && response.data) {
          setAccessToken(response.data.access_token);
          // Fetch user profile
          const profileResponse = await userService.getProfile();
          if (profileResponse.success && profileResponse.data) {
            setUser(profileResponse.data);
          }
        }
      } catch {
        // No valid session, user needs to login
        clearAccessToken();
      } finally {
        setIsLoading(false);
      }
    };

    initAuth();
  }, []);

  const login = useCallback(
    async (data: LoginRequest) => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await authService.login(data);
        if (response.success && response.data) {
          setAccessToken(response.data.access_token);
          // Fetch user profile
          const profileResponse = await userService.getProfile();
          if (profileResponse.success && profileResponse.data) {
            setUser(profileResponse.data);
            router.push("/todos");
          }
        } else {
          setError(response.error || "Login failed");
        }
      } catch (err) {
        setError(getErrorMessage(err));
      } finally {
        setIsLoading(false);
      }
    },
    [router]
  );

  const signup = useCallback(
    async (data: UserCreate) => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await authService.signup(data);
        if (response.success && response.data) {
          setAccessToken(response.data.access_token);
          // Fetch user profile
          const profileResponse = await userService.getProfile();
          if (profileResponse.success && profileResponse.data) {
            setUser(profileResponse.data);
            router.push("/todos");
          }
        } else {
          setError(response.error || "Signup failed");
        }
      } catch (err) {
        setError(getErrorMessage(err));
      } finally {
        setIsLoading(false);
      }
    },
    [router]
  );

  const logout = useCallback(async () => {
    setIsLoading(true);
    try {
      await authService.logout();
    } catch {
      // Ignore logout errors
    } finally {
      clearAccessToken();
      setUser(null);
      setIsLoading(false);
      router.push("/login");
    }
  }, [router]);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated,
        isLoading,
        error,
        login,
        signup,
        logout,
        clearError,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
