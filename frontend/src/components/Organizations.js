import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Typography, List, ListItem, ListItemText, Divider, Container } from '@mui/material';

function Organizations() {
  const [organizations, setOrganizations] = useState([]);
  const [usersData, setUsersData] = useState({});

  useEffect(() => {
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

    fetchOrganizations();
  }, []);

  useEffect(() => {
    const fetchUsersForAllOrgs = async () => {
      const newUsersData = {};

      for (const org of organizations) {
        try {
          const token = localStorage.getItem('token');
            if (!token) {
              console.error('No authorization token found');
              return;
            }
          const response = await api.get(`/list-users/${org.id}`, {
            headers: { Authorization: `Bearer ${token}` }
          });
          console.log(response.data.users)
          newUsersData[org.id] = response.data.users;
        } catch (error) {
          console.error(`Error fetching users for organization ${org.id}:`, error);
          newUsersData[org.id] = [];
        }
      }

      setUsersData(newUsersData);
    };

    if (organizations.length > 0) {
      fetchUsersForAllOrgs();
    }
  }, [organizations]);

  return (
    <div>
      <Container maxWidth="sm" style={{ paddingTop: '25px' }}>
            <Typography variant="h4">Organizations</Typography>
            {organizations.map((org) => (
                <div key={org.id}>
                <Typography variant="h6" style={{ paddingTop: '15px' }}>{org.name}</Typography>
                <List>
                    {(usersData[org.id] || []).map(user => (
                    <ListItem key={user.id}>
                        <ListItemText primary={user.email} />
                    </ListItem>
                    ))}
                </List>
                <Divider />
                </div>
            ))}
      </Container>  
    </div>
  );
}

export default Organizations;
