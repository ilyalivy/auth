import React, { useState } from 'react';
import api from '../services/api';
import { Button, TextField, Typography, Container } from '@mui/material';

function OrganizationCreation() {
  const [organizationName, setOrganizationName] = useState('');
  const [message, setMessage] = useState('');

  const handleOrganizationCreation = async () => {

    try {
      const token = localStorage.getItem('token');
        if (!token) {
          console.error('No authorization token found');
          return;
        }
      const response = await api.post('/create-org', { name: organizationName }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setMessage(response.data.message);
    } catch (error) {
      setMessage(error.response.data.message || 'An error occurred');
    }
  };

  return (
    <div>
      <Container maxWidth="sm" style={{ paddingTop: '25px' }}>
        <Typography variant="h4">Create Organization</Typography>
        <TextField
          label="Organization Name"
          value={organizationName}
          onChange={(e) => setOrganizationName(e.target.value)}
          fullWidth
          margin="normal"
        />
        <Button
          variant="contained"
          color="primary"
          onClick={handleOrganizationCreation}
        >
          Create
        </Button>
        {message && <div>{message}</div>}
      </Container>
    </div>
  );
}

export default OrganizationCreation;