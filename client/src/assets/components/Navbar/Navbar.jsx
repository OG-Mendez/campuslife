import React, { useContext } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './Navbar.css';
import { UserContext } from '../Context/UserContext';
import { Link } from 'react-router-dom';

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user } = useContext(UserContext);

  const handleLoginClick = () => {
    navigate('/login');
  };

  const isAuthPage = ['/login', '/signup', '/forgot-password'].includes(location.pathname);

  return (
    <nav className="navbarC">
      <div className="logo-container">
        <a href="/">
          <img
            src="/logo.svg"
            alt="Logo"
            width="30"
            height="24"
            className="d-inline-block align-text-top"
          />
        </a>
        <h3 className="title">Campuslife</h3>
      </div>
      <div>
        {!isAuthPage && (
          user ? (
            <span className="username">Welcome, {user.username}!</span>
          ) : (
            <button onClick={handleLoginClick} className='signIn'>Sign In</button>
          )
        )}
      </div>
    </nav>
  );
};

export default Navbar;
