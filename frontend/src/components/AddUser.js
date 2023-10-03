import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Button, Typography, Select, MenuItem, FormControl, InputLabel, OutlinedInput, Container } from '@mui/material';

function AddUser() {
  const [users, setUsers] = useState([]);
  const [organizations, setOrganizations] = useState([]);
  const [selectedUserEmail, setSelectedUserEmail] = useState('');
  const [selectedOrganizationName, setSelectedOrganizationName] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const token = localStorage.getItem('token');
          if (!token) {
            console.error('No authorization token found');
            return;
          }
        const response = await api.get('/list-all-users', {
          headers: { Authorization: `Bearer ${token}` }
        });
        setUsers(response.data.users);
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    };

    const fetchOrganizations = async () => {
      try {
        const token = localStorage.getItem('token');
          if (!token) {
            console.error('No authorization token found');
            return;
          }
        const response = await api.get('/list-orgs', {
          headers: { Authorization: `Bearer ${token}` }
        });
        setOrganizations(response.data.organizations);
      } catch (error) {
        console.error('Error fetching organizations:', error);
      }
    };

    fetchUsers();
    fetchOrganizations();

  }, []);
  

  const handleAddUser = async () => {

    try {
      const token = localStorage.getItem('token');
        if (!token) {
          console.error('No authorization token found');
          return;
        }
      const response = await api.post('/add-user-to-org', { user_email: selectedUserEmail, name: selectedOrganizationName }, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      setMessage(response.data.message);
    } catch (error) {
      setMessage(error.response.data.message || 'An error occurred');
    }
  };

  return (
    <div>
      <Container maxWidth="sm" style={{ paddingTop: '25px' }}>

        <Typography variant="h4">Add User to Organization</Typography>
        
        <FormControl variant="outlined" fullWidth margin="normal">
          <InputLabel htmlFor="user-email">User Email</InputLabel>
          <Select
            label="User Email"
            value={selectedUserEmail}
            onChange={(e) => setSelectedUserEmail(e.target.value)}
            input={<OutlinedInput label="User Email" />}
          >
            {users.map(user => (
              <MenuItem key={user.id} value={user.email}>{user.email}</MenuItem>
            ))}
          </Select>
        </FormControl>
        
        <FormControl variant="outlined" fullWidth margin="normal">
          <InputLabel htmlFor="organization-name">Organization Name</InputLabel>
          <Select
            label="Organization Name"
            value={selectedOrganizationName}
            onChange={(e) => setSelectedOrganizationName(e.target.value)}
            input={<OutlinedInput label="Organization Name" />}
          >
            {organizations.map(org => (
              <MenuItem key={org.id} value={org.name}>{org.name}</MenuItem>
            ))}
          </Select>
        </FormControl>
        
        <Button
          variant="contained"
          color="primary"
          onClick={handleAddUser}
        >
          Add User
        </Button>
        {message && <div>{message}</div>}
      </Container>
    </div>
  );
}

export default AddUser;