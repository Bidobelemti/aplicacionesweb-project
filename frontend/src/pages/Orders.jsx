import React, { useEffect, useState } from 'react';
import orderService from '../services/orderService';

const Orders = () => {
    const [orders, setOrders] = useState([]);

    useEffect(() => {
        const fetchOrders = async () => {
            try {
                const response = await orderService.getOrders();
                setOrders(response.data);
            } catch (error) {
                console.error('Error fetching orders:', error);
            }
        };

        fetchOrders();
    }, []);

    return (
        <div>
            <h2>Mis Pedidos</h2>
            {orders.length === 0 ? (
                <p>No tienes pedidos.</p>
            ) : (
                <ul>
                    {orders.map((order) => (
                        <li key={order.id}>
                            <p>
                                <strong>Tipo de pedido:</strong> {order.tipo}
                            </p>
                            <p>
                                <strong>Menú:</strong> {order.menus.join(', ')}
                            </p>
                            <p>
                                <strong>Total:</strong> ${order.totalPago}
                            </p>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default Orders;
