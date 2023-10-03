import React, { useState } from 'react';
import api from '../services/api';
import { Button, TextField, Typography, Container } from '@mui/material';
import { useNavigate } from 'react-router-dom';

function SignIn() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSignIn = async () => {
    try {
      const response = await api.post('/signin', { email, password });
      localStorage.setItem('token', response.data.access_token);
      setMessage('Sign In successful');
      setTimeout(() => {
        navigate('/org-creation');
      }, 1000);
    } catch (error) {
      setMessage(error.response.data.message);
    }
  };

  return (
    <Container maxWidth="sm" style={{ paddingTop: '25px' }}>
      <Typography variant="h4">Sign In</Typography>
      <TextField
        label="Email"
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        fullWidth
        margin="normal"
      />
      <TextField
        label="Password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        fullWidth
        margin="normal"
      />
      <Button
        variant="contained"
        color="primary"
        onClick={handleSignIn}
      >
        Sign In
      </Button>
      {message && <div>{message}</div>}
    </Container>
  );
}

export default SignIn;
