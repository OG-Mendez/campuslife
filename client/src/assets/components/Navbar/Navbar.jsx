import React, { useContext, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './Navbar.css';
import { UserContext } from '../Context/UserContext';
import { Link } from 'react-router-dom';
import Logout from '../Login/Logout';
import { Prev } from 'react-bootstrap/esm/PageItem';

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user } = useContext(UserContext);
  const [showDropdown, setShowDropdown] = useState(false)

  const handleLoginClick = () => {
    navigate('/login');
  };

  const toggleDropdown =  () => {
    setShowDropdown ((prev) => !prev);
  }

  const closeDropdown = () => {
    setShowDropdown(false);
  };

  // const handleMapClick = () => {
  //   navigate('/map');
  // };

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
      {/* <div>
        {!isAuthPage && (
          <button onClick={handleMapClick} className="signIn">
            Show Map
          </button>
        )}
      </div> */}
      <div>
        {!isAuthPage && (
          user ? (
            <div className='U-Name'>
            <span className="username" onClick={toggleDropdown} style={{cursor:'pointer'}}>Welcome, {user.username}! ▼</span>
            { showDropdown && (
              <div className="dropdown-menu1">
                  <div onClick={closeDropdown}>
                    <Logout/>
                    </div>
                    </div>)}
           
            </div>
            
          ) : (
            <button onClick={handleLoginClick} className="signIn">Sign In</button>
          )
        )}
      </div>
    </nav>
  );
};

export default Navbar;
