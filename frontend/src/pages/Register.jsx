import React, { useState } from 'react';
import authService from '../services/authService';

const Register = () => {
    const [name, setName] = useState('');
    const [lastname, setLastname] = useState('');
    const [email, setEmail] = useState('');
    const [phone, setPhone] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        const userData = {
            first_name: name,       
            last_name: lastname,
            email: email,
            phone_number: phone,
            password: password,
        };

        try {
            await authService.register(userData);
            alert('Registro exitoso');
        } catch (error) {
            setError('Error en el registro', error);
        }
    };

    return (
        <div className="register-container">
            <h2>Regístrate</h2>
            {error && <p>{error}</p>}
            <form onSubmit={handleSubmit}>
            <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Nombre"
                required
            />
            <input
                type="text"
                value={lastname}
                onChange={(e) => setLastname(e.target.value)}
                placeholder="Apellido"
                required
            />
            <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email"
                required
            />
            <input
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="Teléfono"
                required
            />
            <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Contraseña"
                required
            />
            <button type="submit">Registrar</button>
            </form>
        </div>
        );

};

export default Register;
