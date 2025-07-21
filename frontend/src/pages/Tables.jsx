import React, { useEffect, useState } from 'react';
import api from '../api'; 

const Tables = () => {
  const [tables, setTables] = useState([]);
  
  // Obtener mesas disponibles
  useEffect(() => {
    const fetchTables = async () => {
      try {
        const response = await api.get('salas/');
        setTables(response.data); 
      } catch (error) {
        console.error('Error fetching tables:', error);
      }
    };
    
    fetchTables();
  }, []);

  return (
    <div>
      <h2>Mesas Disponibles</h2>
      <ul>
        {tables.map(table => (
          <li key={table.id}>
            <h3>{table.number}</h3>
            <p>Capacidad: {table.capacity} personas</p>
            <p>{table.is_available ? 'Mesa disponible' : 'Mesa ocupada'}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Tables;
