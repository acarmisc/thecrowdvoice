import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { logout, getCurrentUser } from '../services/auth';

function Navbar() {
  const navigate = useNavigate();
  const user = getCurrentUser();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="navbar">
      <div className="container">
        <h1>Social Analytics</h1>
        <nav>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/channels">Canali</Link>
          <Link to="/messages">Messaggi</Link>
          <span style={{ marginLeft: '20px', color: '#999' }}>
            Ciao, {user?.username}
          </span>
          <button
            onClick={handleLogout}
            className="btn btn-small"
            style={{ marginLeft: '20px' }}
          >
            Logout
          </button>
        </nav>
      </div>
    </div>
  );
}

export default Navbar;
