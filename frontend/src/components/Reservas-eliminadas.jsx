import React from 'react';
import api from './api';

function EliminarReserva({ reservaId }) {
  const handleDelete = async () => {
    try {
      await api.delete(`/reservas/${reservaId}`);
      console.log('Reserva eliminada');
    } catch (error) {
      console.error('Error al eliminar la reserva:', error);
    }
  };

  return <button onClick={handleDelete}>Eliminar Reserva</button>;
}

export default EliminarReserva;
