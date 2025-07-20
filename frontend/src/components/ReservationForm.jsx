import React, { useState, useEffect } from 'react';
import bookingService from '../services/bookingService';

const ReservationForm = () => {
    const [name, setName] = useState('');
    const [phone, setPhone] = useState('');
    const [peopleQty, setPeopleQty] = useState(1);
    const [selectedTable, setSelectedTable] = useState('');
    const [tables, setTables] = useState([]);

    useEffect(() => {
        const fetchTables = async () => {
            try {
                const response = await bookingService.getAvailableTables();
                setTables(response.data);
            } catch (error) {
                console.error('Error fetching tables:', error);
            }
        };
        fetchTables();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const reservationData = {
            cliente: name,
            telefono: phone,
            cantidad_personas: peopleQty,
            mesa: selectedTable,
            confirmado: true,
        };

        try {
            await bookingService.createReservation(reservationData);
            alert('Reserva realizada con éxito');
        } catch (error) {
            console.error('Error creating reservation:', error);
        }
    };

    return (
        <div>
            <h2>Crear Reserva</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Nombre"
                    required
                />
                <input
                    type="tel"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    placeholder="Teléfono"
                    required
                />
                <input
                    type="number"
                    value={peopleQty}
                    onChange={(e) => setPeopleQty(e.target.value)}
                    min="1"
                    placeholder="Cantidad de personas"
                    required
                />
                <select
                    value={selectedTable}
                    onChange={(e) => setSelectedTable(e.target.value)}
                    required
                >
                    <option value="">Seleccionar mesa</option>
                    {tables.map((table) => (
                        <option key={table.id} value={table.id}>
                            {table.nombre} - {table.capacidad} personas
                        </option>
                    ))}
                </select>
                <button type="submit">Reservar</button>
            </form>
        </div>
    );
};

export default ReservationForm;
