import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor: Injects JWT token into headers if available
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('idea_manager_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

// Response interceptor: Handles global error states like 401 Unauthorized
api.interceptors.response.use((response) => response, (error) => {
    if (error.response && error.response.status === 401) {
        localStorage.removeItem('idea_manager_token');
        window.location.reload(); // Force re-authentication
    }
    return Promise.reject(error);
});

export const login = async (username, password) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    const response = await api.post('/login', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    const { access_token } = response.data;
    localStorage.setItem('idea_manager_token', access_token);
    return response.data;
};

export const register = async (username, password) => {
    const response = await api.post('/register', { username, password });
    return response.data;
};

export const logout = () => {
    localStorage.removeItem('idea_manager_token');
    window.location.reload();
};

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

export const archiveIdea = async (title, archived) => {
    const response = await api.patch(`/ideas/${title}/archive`, null, {
        params: { archived }
    });
    return response.data;
};

export const deleteIdea = async (title) => {
    const response = await api.delete(`/ideas/${title}`);
    return response.data;
};

export const exportIdeas = () => {
    const token = localStorage.getItem('idea_manager_token');
    window.location.href = `${API_BASE_URL}/export?token=${token}`;
};

export const importIdeas = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/import', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

export default api;
