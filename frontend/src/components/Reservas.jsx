import React, { useState, useEffect } from 'react';
import api from '../api'; // Asegúrate de tener configurado axios o fetch en 'api'

function CrearReserva() {
  const [nombreUsuario, setNombreUsuario] = useState('');
  const [salaId, setSalaId] = useState('');
  const [fechaReserva, setFechaReserva] = useState('');
  const [horaInicio, setHoraInicio] = useState('');
  const [horaFin, setHoraFin] = useState('');
  const [tipoOrden, setTipoOrden] = useState(''); // 'eat-in', 'takeaway', 'shipping'
  const [menuItems, setMenuItems] = useState([]); // Para los items del menú
  const [selectedItems, setSelectedItems] = useState([]); // Los items seleccionados por el usuario
  const [direccionEnvio, setDireccionEnvio] = useState('');
  const [telefonoContacto, setTelefonoContacto] = useState('');
  const [error, setError] = useState('');

  // Obtener los items del menú
  useEffect(() => {
    const fetchMenuItems = async () => {
      try {
        const response = await api.get('/menu-items/');
        setMenuItems(response.data);
      } catch (error) {
        console.error('Error al obtener los items del menú', error);
      }
    };
    
    fetchMenuItems();
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();

    // Verificar que el usuario haya seleccionado al menos un item
    if (selectedItems.length === 0) {
      setError('Debes seleccionar al menos un item del menú');
      return;
    }

    // Si el tipo de orden es 'shipping', verificar que se haya ingresado la dirección y teléfono
    if (tipoOrden === 'shipping' && (!direccionEnvio || !telefonoContacto)) {
      setError('Debes ingresar la dirección de envío y el teléfono de contacto');
      return;
    }

    setError(''); // Limpiar mensaje de error si todo es válido

    const nuevaReserva = {
      nombre_usuario: nombreUsuario,
      sala: salaId,
      fecha_reserva: fechaReserva,
      hora_inicio: horaInicio,
      hora_fin: horaFin,
      tipo_orden: tipoOrden,
      items: selectedItems, // Lista de items seleccionados
      direccion_envio: tipoOrden === 'shipping' ? direccionEnvio : null,
      telefono_contacto: tipoOrden === 'shipping' ? telefonoContacto : null,
    };

    try {
      const response = await api.post('/reservas/', nuevaReserva);
      console.log("Reserva creada:", response.data);
      // Opcionalmente, resetear el formulario después de enviar
    } catch (error) {
      console.error("Error al crear la reserva:", error);
    }
  };

  const handleItemSelect = (itemId, cantidad) => {
    setSelectedItems((prevItems) => {
      const existingItem = prevItems.find(item => item.menu_item_id === itemId);
      if (existingItem) {
        existingItem.cantidad = parseInt(cantidad) || 1; // Convertir la cantidad a número entero y evitar valores vacíos
        return [...prevItems];
      }
      return [...prevItems, { menu_item_id: itemId, cantidad: parseInt(cantidad) || 1 }];
    });
  };

  const handleCantidadChange = (itemId, operation) => {
    setSelectedItems(prevItems => {
      return prevItems.map(item => {
        if (item.menu_item_id === itemId) {
          const newCantidad = operation === 'increment' ? item.cantidad + 1 : item.cantidad - 1;
          return { ...item, cantidad: Math.max(newCantidad, 1) }; // Asegurarse de que la cantidad no sea menor que 1
        }
        return item;
      });
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Hacer Reserva</h2>
      <p>Nombre:</p>
      <input
        type="text"
        placeholder="Nombre"
        value={nombreUsuario}
        onChange={(e) => setNombreUsuario(e.target.value)}
        required
      />
      <p>ID de la sala:</p>
      <input
        type="number"
        placeholder="ID de la sala"
        value={salaId}
        onChange={(e) => setSalaId(e.target.value)}
        required
      />
      <p>Fecha:</p>
      <input
        type="date"
        value={fechaReserva}
        onChange={(e) => setFechaReserva(e.target.value)}
        required
      />
      <p>Hora de Inicio:</p>
      <input
        type="time"
        value={horaInicio}
        onChange={(e) => setHoraInicio(e.target.value)}
        required
      />
      <p>Hora de Fin:</p>
      <input
        type="time"
        value={horaFin}
        onChange={(e) => setHoraFin(e.target.value)}
        required
      />

      <div>
        <label>Tipo de Pedido:</label>
        <select onChange={(e) => setTipoOrden(e.target.value)} value={tipoOrden}>
          <option value="">Selecciona el tipo de pedido</option>
          <option value="eat-in">Consumo en el lugar</option>
          <option value="takeaway">Para llevar</option>
          <option value="shipping">Envío a domicilio</option>
        </select>
      </div>

      {tipoOrden && (
        <div>
          <h3>Selecciona los items del menú</h3>
          {menuItems.map((item) => (
            <div key={item.id}>
              <label>{item.nombre} - ${item.precio}</label>
              <div>
                <button type="button" onClick={() => handleCantidadChange(item.id, 'decrement')}>-</button>
                <input
                  type="number"
                  min="1"
                  value={selectedItems.find(i => i.menu_item_id === item.id)?.cantidad || 1}
                  onChange={(e) => handleItemSelect(item.id, e.target.value)}
                />
                <button type="button" onClick={() => handleCantidadChange(item.id, 'increment')}>+</button>
              </div>
            </div>
          ))}
        </div>
      )}

      {tipoOrden === 'shipping' && (
        <div>
          <h3>Detalles de Envío</h3>
          <input
            type="text"
            placeholder="Dirección de Envío"
            value={direccionEnvio}
            onChange={(e) => setDireccionEnvio(e.target.value)}
            required
          />
          <input
            type="text"
            placeholder="Teléfono de Contacto"
            value={telefonoContacto}
            onChange={(e) => setTelefonoContacto(e.target.value)}
            required
          />
        </div>
      )}

      {error && <p style={{ color: 'red' }}>{error}</p>}

      <button type="submit">Crear Reserva</button>
    </form>
  );
}

export default CrearReserva;
