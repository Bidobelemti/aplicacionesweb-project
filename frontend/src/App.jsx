import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'; 
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import MyReservations from './pages/MyReservations';
import Orders from './pages/Orders';
import MenuPage from './pages/MenuPage';
import Header from './components/Header';
import PrivateRoute from './components/PrivateRoute'; // Importar PrivateRoute

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

                    {/* Rutas privadas (solo accesibles si el usuario está autenticado) */}
                    <Route 
                        path="/reservas" 
                        element={<PrivateRoute element={<MyReservations />} />} 
                    />
                    <Route 
                        path="/pedidos" 
                        element={<PrivateRoute element={<Orders />} />} 
                    />

                    {/* Rutas públicas */}
                    <Route path="/menu" element={<MenuPage />} />
                </Routes>
            </div>
        </Router>
    );
};

export default App;
