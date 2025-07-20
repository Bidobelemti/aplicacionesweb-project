import api from './../api';

// Obtener todos los platos del menú
const getMenu = () => {
    return api.get('menu');
};

// Crear un nuevo plato (solo si tienes permisos de administrador)
const createMenuItem = (menuData) => {
    return api.post('menu', menuData);
};

// Obtener todos los camareros disponibles
const getWaiters = () => {
    return api.get('waiters');
};

export default {
    getMenu,
    createMenuItem,
    getWaiters,
};
