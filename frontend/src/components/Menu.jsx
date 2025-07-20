import React, { useEffect, useState } from 'react';
import menuService from '../services/menuService';

const Menu = () => {
    const [menuItems, setMenuItems] = useState([]);

    useEffect(() => {
        const fetchMenu = async () => {
            try {
                const response = await menuService.getMenu();
                setMenuItems(response.data);
            } catch (error) {
                console.error('Error fetching menu:', error);
            }
        };

        fetchMenu();
    }, []);

    return (
        <div>
            <h2>Menú</h2>
            <ul>
                {menuItems.map((item) => (
                    <li key={item.id}>
                        <h3>{item.nombre}</h3>
                        <p>{item.descripcion}</p>
                        <p>Precio: ${item.precio}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Menu;
