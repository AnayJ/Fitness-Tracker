import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authService = {
  register: (name, email, password) =>
    api.post('/auth/register', { name, email, password }),
  
  login: (email, password) =>
    api.post('/auth/login', { email, password }),
  
  verifyToken: (token) =>
    api.post('/auth/verify', { token }),
};

export const userService = {
  getProfile: () => api.get('/users/profile'),
  
  updateProfile: (weight, height, fitness_goal) =>
    api.put('/users/profile', { weight, height, fitness_goal }),
  
  completeOnboarding: (weight, height, fitness_goal) =>
    api.post('/users/onboarding', { weight, height, fitness_goal }),
  
  suggestGoal: (weight, height) =>
    api.post('/users/suggest-goal', null, {
      params: { weight, height },
    }),
};

export const mealService = {
  createMeal: (name, description, calories, protein, carbs, fats) =>
    api.post('/meals/', {
      name,
      description,
      calories,
      protein,
      carbs,
      fats,
    }),
  
  getDailyMeals: (date) =>
    api.get('/meals/daily', { params: { meal_date: date } }),
  
  getMeal: (mealId) => api.get(`/meals/${mealId}`),
  
  updateMeal: (mealId, name, description, calories, protein, carbs, fats) =>
    api.put(`/meals/${mealId}`, {
      name,
      description,
      calories,
      protein,
      carbs,
      fats,
    }),
  
  deleteMeal: (mealId) => api.delete(`/meals/${mealId}`),
};

export const dashboardService = {
  getSummary: (date) =>
    api.get('/dashboard/summary', { params: { meal_date: date } }),
  
  getWeeklyReport: () => api.get('/dashboard/weekly-report'),
  
  getPrediction: () => api.get('/dashboard/prediction'),
  
  getWeeklyTrend: () => api.get('/dashboard/weekly-trend'),
};

export const aiService = {
  chat: (message, history) =>
    api.post('/ai/chat', { message, history }),
};

export default api;
