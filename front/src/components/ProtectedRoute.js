// src/components/ProtectedRoute.js
import React from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('token'); // Verificar si el token está en el localStorage

  // Si no hay token, redirigir al login
  if (!token) {
    return <Navigate to="/" />;
  }

  // Si el token existe, permitir el acceso a la página
  return children;
};

export default ProtectedRoute;
