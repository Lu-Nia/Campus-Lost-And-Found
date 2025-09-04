import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const useAuth = () => {
  return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem('token'));

  // Set up axios defaults when token changes
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      localStorage.setItem('token', token);
    } else {
      delete axios.defaults.headers.common['Authorization'];
      localStorage.removeItem('token');
    }
  }, [token]);

  // Check if user is logged in on app load or when token changes
  useEffect(() => {
    const checkAuth = async () => {
      if (!token) {
        setCurrentUser(null);
        setLoading(false);
        return;
      }

      try {
        const response = await axios.get('http://localhost:8000/auth/me');
        setCurrentUser(response.data);
      } catch (error) {
        console.error('Auth check failed', error);
        setToken(null);
        setCurrentUser(null);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, [token]);

  // Add response interceptor to handle auth errors
  useEffect(() => {
    const interceptor = axios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401 && 
            !error.config.url.includes('/auth/token') &&
            !error.config.url.includes('/auth/register')) {
          setToken(null);
          setCurrentUser(null);
        }
        return Promise.reject(error);
      }
    );

    return () => {
      axios.interceptors.response.eject(interceptor);
    };
  }, []);

  const login = async (studentNumber, password) => {
    const formData = new FormData();
    formData.append('username', studentNumber);
    formData.append('password', password);
    
    try {
      // First, get the token
      const response = await axios.post('http://localhost:8000/auth/token', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      
      const { access_token } = response.data;
      
      // Set the token in localStorage and axios defaults immediately
      localStorage.setItem('token', access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      // Now get user info with the properly set headers
      const userResponse = await axios.get('http://localhost:8000/auth/me');
      setCurrentUser(userResponse.data);
      setToken(access_token); // Update state to trigger other effects
      
      return { success: true };
    } catch (error) {
      setToken(null);
      setCurrentUser(null);
      delete axios.defaults.headers.common['Authorization'];
      localStorage.removeItem('token');
      
      return { 
        success: false, 
        message: error.response?.data?.detail || 'Login failed' 
      };
    }
  };

  const register = async (userData) => {
    try {
      await axios.post('http://localhost:8000/auth/register', userData);
      
      // Auto login after registration
      const loginResult = await login(userData.student_number, userData.password);
      return loginResult;
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.detail || 'Registration failed' 
      };
    }
  };

  const logout = () => {
    setToken(null);
    setCurrentUser(null);
    delete axios.defaults.headers.common['Authorization'];
    localStorage.removeItem('token');
  };

  const updatePassword = async (currentPassword, newPassword) => {
    try {
      await axios.patch('http://localhost:8000/users/password', {
        current_password: currentPassword,
        new_password: newPassword
      });
      return { success: true, message: 'Password updated successfully' };
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.detail || 'Password update failed' 
      };
    }
  };

  const value = {
    currentUser,
    login,
    register,
    logout,
    updatePassword,
    isAuthenticated: !!currentUser
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};