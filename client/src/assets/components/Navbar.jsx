import React from 'react';
import './Navbar.css';

const Navbar = () => {
    return (
      <nav className="navbarC">
        <div className="logo-container">
          <a href="/">
          <img
              src="./logo.svg"
              alt="Logo"
              width="30"
              height="24"
              className="d-inline-block align-text-top"
            />
            </a>
          <h3 className="title">Campuslife</h3>
          
        </div>
      </nav>
    );
  };

export default Navbar;