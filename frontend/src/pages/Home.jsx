import React from 'react';
import { Link, useNavigate } from 'react-router-dom';


const Home = () => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate('/menu'); 
  };

  return (
    <div className="home">
      <h1>Bienvenido a nuestro sistema de reservas y pedidos</h1>
      <p>Explora las opciones disponibles y realiza tu reserva.</p>
      <button className="btn-primary" onClick={handleClick}>Ver Menú</button>
      <nav>
        <Link to="/salas">Salas</Link>
        <Link to="/reservas">Reservas</Link>
        <Link to="/pedidos">Pedidos</Link>
        <Link to="/login">Iniciar Sesión</Link>
        <Link to="/register">Regístrate</Link>
        
      </nav>
      
    </div>
  );
};

export default Home;
