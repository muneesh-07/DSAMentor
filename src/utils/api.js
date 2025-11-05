// src/utils/api.js
import axios from 'axios';

const API_BASE_URL = 'https://muneesh07-dsa-mentor-api.hf.space';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log('🚀 API Request:', config);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log('✅ API Response:', response.data);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error);
    
    if (error.code === 'ECONNABORTED') {
      throw new Error('Request timeout. Please try again.');
    } else if (error.response) {
      throw new Error(`Server error: ${error.response.status}`);
    } else if (error.request) {
      throw new Error('No response from server. Please check your connection.');
    } else {
      throw new Error('An unexpected error occurred.');
    }
  }
);

// Difficulty Analysis API
export const analyzeDifficulty = async (loops, conditionals, nestingDepth, functions, lineCount, complexity, textLength, testCases) => {
  try {
    const response = await api.post('/api/predict', {
      data: [loops, conditionals, nestingDepth, functions, lineCount, complexity, textLength, testCases]
    });
    
    return response.data;
  } catch (error) {
    console.error('Difficulty analysis failed:', error);
    throw error;
  }
};

// Timeline Prediction API
export const predictTimeline = async (studentSkill, problemDifficulty, problemComplexity, problemLength) => {
  try {
    const response = await api.post('/api/predict', {
      data: [studentSkill, problemDifficulty, problemComplexity, problemLength]
    });
    
    return response.data;
  } catch (error) {
    console.error('Timeline prediction failed:', error);
    throw error;
  }
};

// Mistake Classification API
export const classifyMistake = async (loops, conditionals, nestingDepth, lineCount, complexity, hasRecursion, functions, problemDifficulty) => {
  try {
    const response = await api.post('/api/predict', {
      data: [loops, conditionals, nestingDepth, lineCount, complexity, hasRecursion, functions, problemDifficulty]
    });
    
    return response.data;
  } catch (error) {
    console.error('Mistake classification failed:', error);
    throw error;
  }
};

export default api;
