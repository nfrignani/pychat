import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from './axios';

const Login = ({ onLogin }) => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');


const handleSubmit = async (e) => {
  e.preventDefault();
  const form = e.currentTarget;
  const email = form.elements.email.value;
  const password = form.elements.password.value;
  const data = { email, password };
  console.log('Effettuando chiamata API...');
  try {
    const res = await axios.post('/api/auth/login', data);
    console.log('Risposta API:', res);
    localStorage.setItem('token', res.data.access_token);
    alert(`Token: ${res.data.access_token}`); // TODO remove
    // onLogin();
    // window.location.href = '/chat'; // aggiungi questa riga per reindirizzare l'utente alla pagina principale dopo il login
    navigate('/chat'); // utilizza navigate per navigare alla pagina /chat
    //return <Navigate to="/chat" replace />;
  } catch (err) {
    console.error('Errore API:', err);
  }
};

  return (
    <form onSubmit={(e) => handleSubmit(e)}>
      <input type="email"  name="email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <input type="password"  name="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <input type="submit" value="Login" />
    </form>
  );
};

export default Login;