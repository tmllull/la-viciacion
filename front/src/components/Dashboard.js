// src/components/Dashboard.js
import React, { useState, useEffect } from 'react';

const Dashboard = () => {
  const [items, setItems] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');

  // Función para hacer la primera llamada a la API y obtener los IDs
  const fetchItems = async () => {
    const token = localStorage.getItem('token'); // Recuperar el token del localStorage

    try {
      const response = await fetch('https://example.com/api/items', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,  // Incluir el token en los headers
        },
      });

      if (response.ok) {
        const data = await response.json();
        // Aquí tenemos solo los IDs, ahora necesitamos obtener los nombres
        setItems(data);
      } else {
        setErrorMessage('Error al obtener los datos');
      }
    } catch (error) {
      setErrorMessage('Error en la comunicación con el servidor');
    }
  };

  // Función para obtener el nombre de un elemento por su ID
  const fetchItemName = async (id) => {
    const token = localStorage.getItem('token');

    try {
      const response = await fetch(`https://example.com/api/items/${id}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,  // Incluir el token en los headers
        },
      });

      if (response.ok) {
        const data = await response.json();
        return data.name; // Suponemos que la respuesta de la API contiene el nombre en data.name
      } else {
        setErrorMessage('Error al obtener el nombre del elemento');
        return null;
      }
    } catch (error) {
      setErrorMessage('Error en la comunicación con el servidor');
      return null;
    }
  };

  // Efecto para cargar los items y sus nombres al montar el componente
  useEffect(() => {
    const loadItemsWithNames = async () => {
      await fetchItems(); // Primero, obtener los IDs de los items

      const updatedItems = await Promise.all(
        items.map(async (item) => {
          const name = await fetchItemName(item.id); // Obtener el nombre para cada ID
          return { ...item, name }; // Devolver el objeto con el nombre agregado
        })
      );

      setItems(updatedItems); // Actualizar el estado con los items y sus nombres
    };

    loadItemsWithNames();
  }, []);

  return (
    <div>
      <h1>Dashboard</h1>

      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}

      {items.length > 0 ? (
        <ul>
          {items.map((item) => (
            <li key={item.id}>
              {item.name ? item.name : 'Cargando nombre...'}
            </li>
          ))}
        </ul>
      ) : (
        <p>No hay elementos para mostrar</p>
      )}
    </div>
  );
};

export default Dashboard;
