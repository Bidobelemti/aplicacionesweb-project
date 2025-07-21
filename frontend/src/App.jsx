import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'; 
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import MyReservations from './pages/MyReservations';
import Orders from './pages/Orders';
import MenuPage from './pages/MenuPage';
import Header from './components/Header';
import PrivateRoute from './components/PrivateRoute'; 
import Salas from './pages/Tables';
import Reservas from './components/Reservas';
import ReservationForm from './components/ReservationForm';
import UserReservations from './components/UserReservations';

const App = () => {
    return (
        <Router>
            {/* Este Header estará en todas las páginas */}
            <Header />

            {/* Contenedor principal donde se renderizan las páginas según la ruta */}
            <div className="container">
                <Routes>
                    {/* Página principal (Home) */}
                    <Route path="/" element={<Home />} />

                    {/* Rutas de autenticación */}
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />

                    <Route 
                        path="/pedidos" 
                        element={<PrivateRoute element={<Orders />} />} 
                    />

                    {/* Rutas públicas */}
                    <Route path="/menu" element={<MenuPage />} />
                    <Route path="/salas" element={<Salas />} />
                    <Route path="/reservas" element={<Reservas />} />
                    <Route path="/mis-reservas" element={<UserReservations />} />
                </Routes>
            </div>
        </Router>
    );
};

export default App;
