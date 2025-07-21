import React, { useState, useEffect } from 'react';
import api from '../api'; 

const ReservationForm = () => {
  const [name, setName] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [peopleQty, setPeopleQty] = useState(1);
  const [selectedTables, setSelectedTables] = useState([]);
  const [availableTables, setAvailableTables] = useState([]);
  
  useEffect(() => {
    const fetchTables = async () => {
      try {
        const response = await api.get('salas/');
        setAvailableTables(response.data.filter(table => table.is_available)); // Asegúrate de que 'is_available' es la propiedad correcta
      } catch (error) {
        console.error('Error fetching tables:', error);
      }
    };
    
    fetchTables();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const reservationData = {
      name,
      phoneNumber,
      peopleQty,
      tables: selectedTables,
    };

    try {
      await api.post('reservas/', reservationData);
      alert('Reserva realizada con éxito');
    } catch (error) {
      console.error('Error creating reservation:', error);
    }
  };

  const handleTableSelect = (tableId) => {
    setSelectedTables(prevSelected => 
      prevSelected.includes(tableId)
        ? prevSelected.filter(id => id !== tableId)
        : [...prevSelected, tableId]
    );
  };

  return (
    <div>
      <h2>Hacer Reserva</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Nombre"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Teléfono"
          value={phoneNumber}
          onChange={(e) => setPhoneNumber(e.target.value)}
          required
        />
        <input
          type="number"
          placeholder="Cantidad de personas"
          value={peopleQty}
          onChange={(e) => setPeopleQty(e.target.value)}
          required
        />
        <div>
          <h3>Selecciona las mesas:</h3>
          {availableTables.map((table) => (
            <label key={table.id}>
              <input
                type="checkbox"
                value={table.id}
                onChange={() => handleTableSelect(table.id)}
              />
              {table.number} - {table.capacity} personas
            </label>
          ))}
        </div>
        <button type="submit">Hacer Reserva</button>
      </form>
    </div>
  );
};

export default ReservationForm;
