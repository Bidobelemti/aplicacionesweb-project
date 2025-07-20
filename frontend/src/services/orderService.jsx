import api from './../api';

// Obtener todos los pedidos
const getOrders = () => {
    return api.get('orders');
};

// Crear un pedido Eatin
const createEatinOrder = (orderData) => {
    return api.post('orders/eatin', orderData);
};

// Crear un pedido TakeAway
const createTakeAwayOrder = (orderData) => {
    return api.post('orders/takeaway', orderData);
};

// Crear un pedido Shipping
const createShippingOrder = (orderData) => {
    return api.post('orders/shipping', orderData);
};

export default {
    getOrders,
    createEatinOrder,
    createTakeAwayOrder,
    createShippingOrder,
};
