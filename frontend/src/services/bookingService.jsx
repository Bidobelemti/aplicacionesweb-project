import api from './../api';

const getUserReservations = () => {
    return api.get('http://localhost:8000/api/salas');  // Verifica que la URL esté correcta
};


export default {
    getUserReservations,
};
