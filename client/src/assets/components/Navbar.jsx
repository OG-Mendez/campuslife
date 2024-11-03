import React from 'react';
import './Navbar.css';

const Navbar = () => {
    return (
      <nav className="navbar">
        <div className="logo-container">
          <span className="logo">
          <img
              src="./src/assets/images/Campuslife_logo.png"
              alt="Logo"
              width="30"
              height="24"
              className="d-inline-block align-text-top"
            />
          </span>
          <h3 className="title">Campuslife</h3>
        </div>
      </nav>
    );
  };

export default Navbar;