import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '@mui/material';

function Nav() {
  const navigate = useNavigate();
  const isSignedIn = localStorage.getItem('token') !== null;

  const handleSignOut = () => {
    localStorage.removeItem('token');
    navigate('/signin');
  };

  return (
    <nav style={{ padding: '20px' }}> 
      {!isSignedIn && <Button component={Link} to="/signup" sx={{ fontSize: '18px', marginRight: '10px' }}>Sign Up</Button>}
      {!isSignedIn && <Button component={Link} to="/signin" sx={{ fontSize: '18px', marginRight: '10px' }}>Sign In</Button>}
      {isSignedIn && <Button component={Link} to="/org-creation" sx={{ fontSize: '18px', marginRight: '10px' }}>Create Organization</Button>}
      {isSignedIn && <Button component={Link} to="/add-user" sx={{ fontSize: '18px', marginRight: '10px' }}>Add User</Button>}
      {isSignedIn && <Button component={Link} to="/organizations" sx={{ fontSize: '18px', marginRight: '10px' }}>Organizations</Button>}
      {isSignedIn && <Button component={Link} to="/signin" onClick={handleSignOut} sx={{ fontSize: '18px', marginRight: '10px' }}>Sign Out</Button>}
    </nav>
  );
}

export default Nav;
