import React, { useState, useEffect } from 'react';
import orderService from '../services/orderService';
import menuService from '../services/menuService';

const OrderForm = () => {
    const [orderType, setOrderType] = useState('eatin');
    const [selectedMenuItems, setSelectedMenuItems] = useState([]);
    const [menuItems, setMenuItems] = useState([]);
    
    useEffect(() => {
        const fetchMenuItems = async () => {
            try {
                const response = await menuService.getMenu();
                setMenuItems(response.data);
            } catch (error) {
                console.error('Error fetching menu items:', error);
            }
        };

        fetchMenuItems();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const orderData = {
            tipo: orderType,
            menus: selectedMenuItems,
        };

        try {
            if (orderType === 'eatin') {
                await orderService.createEatinOrder(orderData);
            } else if (orderType === 'takeaway') {
                await orderService.createTakeAwayOrder(orderData);
            } else if (orderType === 'shipping') {
                await orderService.createShippingOrder(orderData);
            }
            alert('Pedido realizado con éxito');
        } catch (error) {
            console.error('Error creating order:', error);
        }
    };

    const handleMenuItemChange = (menuId) => {
        setSelectedMenuItems((prevItems) =>
            prevItems.includes(menuId)
                ? prevItems.filter((id) => id !== menuId)
                : [...prevItems, menuId]
        );
    };

    return (
        <div className="order-form">
            <h2>Crear Pedido</h2>
            <form onSubmit={handleSubmit}>
            <label>
                Tipo de Pedido:
                <select value={orderType} onChange={(e) => setOrderType(e.target.value)}>
                <option value="eatin">Comer en el lugar</option>
                <option value="takeaway">Para llevar</option>
                <option value="shipping">Envio a domicilio</option>
                </select>
            </label>

            <h3>Menú</h3>
            {menuItems.map((item) => (
                <div className="menu-item" key={item.id}>
                <input
                    type="checkbox"
                    id={item.id}
                    onChange={() => handleMenuItemChange(item.id)}
                />
                <label htmlFor={item.id}>{item.nombre}</label>
                </div>
            ))}

            <button type="submit">Realizar Pedido</button>
            </form>
        </div>
    );

};

export default OrderForm;
