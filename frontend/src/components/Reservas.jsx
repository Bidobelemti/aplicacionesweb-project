import React, { useState } from 'react';
import api from './api';  // Importa la instancia de Axios

function CrearReserva() {
  const [nombreUsuario, setNombreUsuario] = useState('');
  const [salaId, setSalaId] = useState('');
  const [fechaReserva, setFechaReserva] = useState('');
  const [horaInicio, setHoraInicio] = useState('');
  const [horaFin, setHoraFin] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();

    const nuevaReserva = {
      nombre_usuario: nombreUsuario,
      sala: salaId,
      fecha_reserva: fechaReserva,
      hora_inicio: horaInicio,
      hora_fin: horaFin,
    };

    try {
      const response = await api.post('/reservas/', nuevaReserva);
      console.log("Reserva creada:", response.data);
    } catch (error) {
      console.error("Error al crear la reserva:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Nombre"
        value={nombreUsuario}
        onChange={(e) => setNombreUsuario(e.target.value)}
      />
      <input
        type="number"
        placeholder="ID de la sala"
        value={salaId}
        onChange={(e) => setSalaId(e.target.value)}
      />
      <input
        type="date"
        value={fechaReserva}
        onChange={(e) => setFechaReserva(e.target.value)}
      />
      <input
        type="time"
        value={horaInicio}
        onChange={(e) => setHoraInicio(e.target.value)}
      />
      <input
        type="time"
        value={horaFin}
        onChange={(e) => setHoraFin(e.target.value)}
      />
      <button type="submit">Crear Reserva</button>
    </form>
  );
}

export default CrearReserva;
