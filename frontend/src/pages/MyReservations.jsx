import React, { useEffect, useState } from 'react';
import bookingService from '../services/bookingService';

const MyReservations = () => {
    const [reservations, setReservations] = useState([]);

    useEffect(() => {
        const fetchReservations = async () => {
            try {
                const response = await bookingService.getUserReservations();
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
            {reservations.length === 0 ? (
                <p>No tienes reservas.</p>
            ) : (
                <ul>
                    {reservations.map((reservation) => (
                        <li key={reservation.id}>
                            <p>
                                <strong>Mesa:</strong> {reservation.mesa.nombre}
                            </p>
                            <p>
                                <strong>Fecha:</strong> {reservation.fecha}
                            </p>
                            <p>
                                <strong>Hora:</strong> {reservation.hora}
                            </p>
                            <p>
                                <strong>Cantidad de personas:</strong>{' '}
                                {reservation.cantidad_personas}
                            </p>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default MyReservations;
