import api from './../api';

// Obtener las mesas disponibles
const getAvailableTables = () => {
    return api.get('salas');
};

// Crear una nueva reserva
const createReservation = (reservationData) => {
    return api.post('reservas', reservationData);
};

// Obtener reservas del usuario autenticado
const getUserReservations = () => {
    return api.get('reservas/mis-reservas');
};

// Eliminar una reserva
const deleteReservation = (reservationId) => {
    return api.delete(`reservas/${reservationId}`);
};

export default {
    getAvailableTables,
    createReservation,
    getUserReservations,
    deleteReservation,
};
