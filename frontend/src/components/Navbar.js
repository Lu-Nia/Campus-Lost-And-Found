import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useLogout } from '../hooks/useLogout';
import '../styles/Navbar.css';

const Navbar = () => {
  const { currentUser } = useAuth();
  const handleLogout = useLogout();
  const [showDropdown, setShowDropdown] = useState(false);

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <h2>Campus Digital Lost & Found</h2>
      </div>
      
      <div className="navbar-menu">
        <div className="navbar-user">
          <span>Welcome, {currentUser?.name}</span>
          <div 
            className="user-dropdown-toggle"
            onClick={() => setShowDropdown(!showDropdown)}
          >
            👤
          </div>
          
          {showDropdown && (
            <div className="user-dropdown">
              
              <button onClick={handleLogout}>Logout</button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;