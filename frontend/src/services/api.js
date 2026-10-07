import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

// Automatically attach JWT token to outgoing requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('careerpath_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

// ==============================================================================
// AUTHENTICATION APIs
// ==============================================================================
export const registerUser = async (userData) => {
  return api.post('/api/auth/register', userData);
};

export const loginUser = async (credentials) => {
  return api.post('/api/auth/login', credentials);
};

export const getCurrentUser = async () => {
  return api.get('/api/auth/me');
};

export const updateUserProfile = async (profileData) => {
  return api.put('/api/auth/profile', profileData);
};

export const verifyEmail = async (token) => {
  return api.get('/api/auth/verify-email', { params: { token } });
};

export const resendVerification = async (email) => {
  return api.post('/api/auth/resend-verification', { email });
};

// ==============================================================================
// INSTITUTION & UNIVERSITY ANALYTICS APIs
// ==============================================================================
export const getInstitutionAnalytics = async (institution = 'IIT Madras', department = 'Computer Science & Engineering') => {
  return api.get('/api/institution/analytics', {
    params: { institution, department }
  });
};

// ==============================================================================
// CORE TALENT & CAREER APIs
// ==============================================================================
export const uploadResume = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/api/resume/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const normalizeSkills = async (skills) => {
  return api.post('/api/skills/normalize', { skills });
};

export const getRoles = async () => {
  return api.get('/api/roles');
};

export const getRoleDetails = async (roleId) => {
  return api.get(`/api/roles/${roleId}`);
};

export const analyzeGap = async (userSkills, targetRoleId) => {
  return api.post('/api/analysis/gap', {
    user_skills: userSkills,
    target_role_id: String(targetRoleId),
    userSkills: userSkills,
    targetRoleId: String(targetRoleId)
  });
};

export const getRecommendations = async (userSkills, education = [], experience = {}) => {
  return api.post('/api/recommendations', {
    user_skills: userSkills,
    user_education: education,
    user_experience: experience,
    userSkills: userSkills,
    education: education,
    experience: experience
  });
};

export const getRoadmap = async (missingSkills) => {
  return api.post('/api/roadmap', {
    missing_skills: missingSkills,
    missingSkills: missingSkills
  });
};

export const downloadReport = async (reportData) => {
  return api.post('/api/report/pdf', reportData, {
    responseType: 'blob',
  });
};

// ==============================================================================
// SAS CU HACKATHON: TALENT INTELLIGENCE & PREDICTIVE ML APIs
// ==============================================================================
export const getMarketOverview = async () => {
  return api.get('/api/talent/market-overview');
};

export const predictJDSHike = async (scores) => {
  return api.post('/api/talent/jds-hike-predict', scores);
};

export const predictSDSLeadership = async (scores) => {
  return api.post('/api/talent/sds-leadership-predict', scores);
};

export const estimateMarketSalary = async (params) => {
  return api.post('/api/talent/salary-benchmark', params);
};

export default api;
