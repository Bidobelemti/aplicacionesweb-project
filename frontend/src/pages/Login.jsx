import React, { useState } from 'react';
import authService from '../services/authService';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const history = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const user = await authService.login({ email, password });
            if (user) {
                history.push('/dashboard'); // O donde redirijas después de hacer login
            }
        } catch (error) {
            setError('Error al iniciar sesión. Por favor verifique sus credenciales.', error);
        }
    };

    return (
        <div className="login-container">
            <h2>Iniciar Sesión</h2>
            {error && <p>{error}</p>}
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
            <button type="submit">Login</button>
            </form>
        </div>
        );

};

export default Login;
