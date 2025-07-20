import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'


// Importa los estilos globales
import './assets/styles/header.css'; 
import './assets/styles/home.css';
import './assets/styles/menu.css';
import './assets/styles/login.css';
import './assets/styles/register.css';
import './assets/styles/reservations.css';
import './assets/styles/orderForm.css';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
