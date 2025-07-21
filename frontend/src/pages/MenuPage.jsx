import React, { useEffect, useState } from 'react';
import menuService from '../services/menuService';
import OrderForm from '../components/OrderForm';  // Importa el formulario de pedido

const MenuPage = () => {
    const [menuItems, setMenuItems] = useState([]);
    const [selectedMenu, setSelectedMenu] = useState([]);
    const [total, setTotal] = useState(0);

    // Cargar los ítems del menú desde la API
    useEffect(() => {
        const fetchMenu = async () => {
            try {
                const response = await menuService.getMenu();
                setMenuItems(response.data);
            } catch (error) {
                console.error('Error al cargar el menú', error);
            }
        };

        fetchMenu();
    }, []);

    // Añadir un menú al pedido
    const addMenuToOrder = (menuItem) => {
        setSelectedMenu((prevState) => {
            const newState = [...prevState, menuItem];
            setTotal(newState.reduce((acc, item) => acc + item.precio, 0));  // Calcula el total
            return newState;
        });
    };

    // Eliminar un menú del pedido
    const removeMenuFromOrder = (menuItem) => {
        setSelectedMenu((prevState) => {
            const newState = prevState.filter((item) => item.id !== menuItem.id);
            setTotal(newState.reduce((acc, item) => acc + item.precio, 0));  // Recalcular el total
            return newState;
        });
    };

    return (
        <div className="menu-page">
            <h1>Menú</h1>
            <div className="menu-list">
            <h2>Platos Disponibles</h2>
            <ul>
                {menuItems.map((item) => (
                <li key={item.id}>
                    <div>
                    <h3>{item.nombre}</h3>
                    <p>{item.activo ? 'Disponible' : 'No Disponible'}</p>
                    </div>
                    <div>
                    <p>${item.precio}</p>
                    <button onClick={() => addMenuToOrder(item)}>
                        Añadir al Pedido
                    </button>
                    </div>
                </li>
                ))}
            </ul>
            </div>

            <hr />

            <div className="order-summary">
            <h2>Pedido Actual</h2>
            <ul>
                {selectedMenu.map((item) => (
                <li key={item.id}>
                    <div>
                    <h3>{item.nombre}</h3>
                    </div>
                    <div>
                    <p>${item.precio}</p>
                    <button onClick={() => removeMenuFromOrder(item)}>Eliminar</button>
                    </div>
                </li>
                ))}
            </ul>

            <h3>Total: ${total}</h3>

            <hr />

            <OrderForm type="eatin" menus={selectedMenu} total={total} />
            </div>
        </div>
        );

};

export default MenuPage;
