import api from './api';

export const getChannels = async () => {
  const response = await api.get('/channels/accounts/');
  return response.data;
};

export const getFacebookAuthUrl = async () => {
  const response = await api.get('/channels/facebook/auth-url/');
  return response.data.auth_url;
};

export const getInstagramAuthUrl = async () => {
  const response = await api.get('/channels/instagram/auth-url/');
  return response.data.auth_url;
};

export const getLinkedInAuthUrl = async () => {
  const response = await api.get('/channels/linkedin/auth-url/');
  return response.data.auth_url;
};

export const getTikTokAuthUrl = async () => {
  const response = await api.get('/channels/tiktok/auth-url/');
  return response.data.auth_url;
};

export const deleteChannel = async (channelId) => {
  const response = await api.delete(`/channels/accounts/${channelId}/`);
  return response.data;
};

export const syncMessages = async (channelId) => {
  const response = await api.post(`/messages/sync/${channelId}/`);
  return response.data;
};
