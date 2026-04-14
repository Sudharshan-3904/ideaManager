import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const getIdeas = async () => {
    const response = await api.get('/ideas');
    return response.data;
};

export const getIdea = async (title) => {
    const response = await api.get(`/ideas/${title}`);
    return response.data;
};

export const createIdea = async (idea) => {
    const response = await api.post('/ideas', idea);
    return response.data;
};

export const updateIdea = async (originalTitle, idea) => {
    const response = await api.put(`/ideas/${originalTitle}`, idea);
    return response.data;
};

export const deleteIdea = async (title) => {
    const response = await api.delete(`/ideas/${title}`);
    return response.data;
};

export default api;
