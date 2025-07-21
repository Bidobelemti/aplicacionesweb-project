import React, { useEffect, useState } from 'react';
import api from './api';  // Importa la instancia de Axios

function Salas() {
  const [salas, setSalas] = useState([]);

  useEffect(() => {
    const fetchSalas = async () => {
      try {
        const response = await api.get('/salas');
        setSalas(response.data);
      } catch (error) {
        console.error("Error al obtener las salas:", error);
      }
    };

    fetchSalas();
  }, []);

  return (
    <div>
      <h1>Salas Disponibles</h1>
      <ul>
        {salas.map((sala) => (
          <li key={sala.id}>
            {sala.nombre} (Capacidad: {sala.capacidad})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Salas;
