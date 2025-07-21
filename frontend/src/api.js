import axios from 'axios';

// URL base de tu API Django
const api= axios.create({
    baseURL: 'http://localhost:8000/api/'
});


// Interceptor para añadir el token en cada request (si existe)
api.interceptors.request.use(config => {
  const user = JSON.parse(localStorage.getItem('user'));
  if (user && user.token) {
    config.headers.Authorization = `Token ${user.token}`;
  }
  return config;
}, error => Promise.reject(error));

// Obtener todas las reservas
export const getReservas = async () => {
  try {
    const response = await axios.get(api);
    return response.data;
  } catch (error) {
    console.error("Error al obtener reservas:", error);
    throw error;
  }
};

// Crear una nueva reserva
export const crearReserva = async (reserva) => {
  try {
    const response = await axios.post(api, reserva);
    return response.data;
  } catch (error) {
    console.error("Error al crear la reserva:", error);
    throw error;
  }
};

export default api;