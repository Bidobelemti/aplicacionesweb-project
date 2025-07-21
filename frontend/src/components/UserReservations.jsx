import React, { useState, useEffect } from 'react';
import api from '../api'; 

const UserReservations = () => {
  const [reservations, setReservations] = useState([]);

  useEffect(() => {
    const fetchReservations = async () => {
      try {
        const response = await api.get('reservas/');
        setReservations(response.data); 
      } catch (error) {
        console.error('Error fetching reservations:', error);
      }
    };
    
    fetchReservations();
  }, []);

  return (
    <div>
      <h2>Mis Reservas</h2>
      {reservations.length > 0 ? (
        <ul>
          {reservations.map((reservation) => (
            <li key={reservation.id}>
              <h3>Reserva para {reservation.name}</h3>
              <p>Fecha: {new Date(reservation.date).toLocaleString()}</p>
              <p>Mesas seleccionadas: {reservation.tables.map(table => table.name).join(', ')}</p>
              <p>{reservation.confirmed ? 'Confirmada' : 'Pendiente'}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p>No tienes reservas.</p>
      )}
    </div>
  );
};

export default UserReservations;
