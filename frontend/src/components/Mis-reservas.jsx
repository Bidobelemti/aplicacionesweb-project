import React, { useEffect, useState } from 'react';
import api from './api';  // Importa la instancia de Axios

function MisReservas() {
  const [reservas, setReservas] = useState([]);

  useEffect(() => {
    const fetchMisReservas = async () => {
      try {
        const response = await api.get('/reservas/mis-reservas');
        setReservas(response.data);
      } catch (error) {
        console.error("Error al obtener mis reservas:", error);
      }
    };

    fetchMisReservas();
  }, []);

  return (
    <div>
      <h1>Mis Reservas</h1>
      <ul>
        {reservas.map((reserva) => (
          <li key={reserva.id}>
            {reserva.sala.nombre} - {reserva.fecha_reserva} ({reserva.hora_inicio} a {reserva.hora_fin})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default MisReservas;
