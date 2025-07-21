import api from './../api';

const register = (userData) => {
    return api.post('http://localhost:8000/api/users/register/', userData);
};

const login = (credentials) => {
    return api.post('http://localhost:8000/api/users/login/', credentials)
        .then(response => {
            if (response.data.token) {
                localStorage.setItem('user', JSON.stringify(response.data));
            }
            return response.data;
        });
};

const logout = () => {
    localStorage.removeItem('user');
};

const getCurrentUser = () => {
    return JSON.parse(localStorage.getItem('user'));
};

export default {
    register,
    login,
    logout,
    getCurrentUser,
};
