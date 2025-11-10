import api from './api';

export const getMessages = async (params = {}) => {
  const response = await api.get('/messages/', { params });
  return response.data;
};

export const getSentimentStats = async () => {
  const response = await api.get('/sentiment/stats/');
  return response.data;
};

export const batchAnalyze = async () => {
  const response = await api.post('/sentiment/batch-analyze/');
  return response.data;
};

export const analyzeMessage = async (messageId) => {
  const response = await api.post(`/sentiment/analyze/${messageId}/`);
  return response.data;
};
