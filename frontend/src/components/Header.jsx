import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import authService from '../services/authService';
import '../assets/styles/header.css';

const Header = () => {
    const history = useNavigate();
    const user = authService.getCurrentUser();

    const handleLogout = () => {
        authService.logout();
        history('/login');
    };

    return (
        <header className="header">
            <nav className="left-nav">
                <Link to="/">Home</Link>
            </nav>
            <nav className="right-nav">
                {user ? (
                <>
                    <Link to="/mis-reservas">Mis Reservas</Link>
                    <Link to="/pedidos">Mis Pedidos</Link>
                    <button onClick={handleLogout}>Cerrar sesión</button>
                </>
                ) : (
                <>
                    <Link to="/login">Iniciar Sesión</Link>
                    <Link to="/register">Regístrate</Link>
                </>
                )}
            </nav>
            </header>

    );
};

export default Header;
