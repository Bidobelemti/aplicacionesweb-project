import React, { useState } from 'react';
import authService from '../services/authService';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [successMessage, setSuccessMessage] = useState(''); 
    const navigate = useNavigate(); 

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const user = await authService.login({ email, password });
            if (user) {
                setSuccessMessage('Inicio de sesión exitoso. Redirigiendo...');
                setError('');
                setTimeout(() => {
                    navigate('/'); 
                }, 1000); 
            }
        } catch (error) {
            setError(error.message || 'Error al iniciar sesión. Por favor verifique sus credenciales.');
            setSuccessMessage('');
            console.error(error); 
        }
    };

    return (
        <div className="login-container">
            <h2>Iniciar Sesión</h2>
            {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>} {/* Mensaje de éxito */}
            {error && <p style={{ color: 'red' }}>{error}</p>} {/* Mostrar el mensaje de error */}
            <form onSubmit={handleSubmit}>
                <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Email"
                    required
                />
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                    required
                />
                <button type="submit">Iniciar Sesión</button>
            </form>
        </div>
    );
};

export default Login;
