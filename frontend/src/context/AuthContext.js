import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback
} from 'react';
import { authService, userService } from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('access_token'));
  const [loading, setLoading] = useState(true);

const verifyToken = useCallback(async () => {
  try {
    const response = await authService.verifyToken(token);

    if (response.data.valid) {
      // fetch full profile so UI shows name and other fields
      try {
        const profile = await userService.getProfile();
        setUser(profile.data);
      } catch (err) {
        // fallback to minimal info
        setUser({ id: response.data.user_id });
      }
    }
  } catch (error) {
    localStorage.removeItem('access_token');
    setToken(null);
  } finally {
    setLoading(false);
  }
}, [token]);

useEffect(() => {
  if (token) {
    verifyToken();
  } else {
    setLoading(false);
  }
}, [token, verifyToken]);

  const register = async (name, email, password) => {
    try {
      const response = await authService.register(name, email, password);
      const { access_token, user } = response.data;
      
      localStorage.setItem('access_token', access_token);
      setToken(access_token);
      setUser(user);
      
      return user;
    } catch (error) {
      throw error.response?.data || error;
    }
  };

  const login = async (email, password) => {
    try {
      const response = await authService.login(email, password);
      const { access_token, user } = response.data;
      
      localStorage.setItem('access_token', access_token);
      setToken(access_token);
      setUser(user);
      
      return user;
    } catch (error) {
      throw error.response?.data || error;
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setToken(null);
    setUser(null);
  };

  const updateUser = (userData) => {
    setUser({ ...user, ...userData });
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        register,
        login,
        logout,
        updateUser,
        isAuthenticated: !!token,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
