import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL 
  ? `${process.env.REACT_APP_API_URL}/api` 
  : '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const parseResume = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  return api.post('/parse-resume', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const analyzeForm = async (formUrl) => {
  return api.post('/analyze-form', { form_url: formUrl });
};

export const fillForm = async (file, formUrl) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('form_url', formUrl);
  
  return api.post('/fill-form', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    timeout: 10000, // Short timeout for task start
  });
};

export const getTaskStatus = async (taskId) => {
  return api.get(`/task-status/${taskId}`);
};

export const pollTaskStatus = async (taskId, onProgress) => {
  return new Promise((resolve, reject) => {
    const poll = async () => {
      try {
        const response = await getTaskStatus(taskId);
        const { status, progress, result, error, message } = response.data;
        
        if (onProgress) onProgress(progress, message);
        
        if (status === 'completed') {
          resolve(result);
        } else if (status === 'error') {
          reject(new Error(error));
        } else {
          setTimeout(poll, 2000); // Poll every 2 seconds
        }
      } catch (err) {
        reject(err);
      }
    };
    poll();
  });
};

export const healthCheck = async () => {
  return api.get('/health');
};