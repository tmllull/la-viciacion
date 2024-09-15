// src/components/Login.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();  // Hook para redirigir

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const clientId = 'your-client-id';
    const clientSecret = 'your-client-secret';

    const bodyData = new URLSearchParams();
    bodyData.append('username', username);
    bodyData.append('password', password);
    bodyData.append('grant_type', 'password');
    bodyData.append('client_id', clientId);
    bodyData.append('client_secret', clientSecret);

    try {
      const response = await fetch('http://localhost:5000/api/v1/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: bodyData.toString(),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem('token', data.access_token);
        alert('Login exitoso');
        // Redirigir al dashboard
        navigate('/dashboard');  // Redirección después del login exitoso
      } else {
        setErrorMessage(data.error_description || 'Credenciales incorrectas');
      }
    } catch (error) {
      setErrorMessage('Error en la autenticación');
    }
  };

  return (
    <div>
      <h2>Iniciar sesión</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Usuario:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div>
          <label>Contraseña:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="submit">Iniciar sesión</button>
      </form>
      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
    </div>
  );
};

export default Login;
