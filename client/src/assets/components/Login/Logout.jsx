import React, { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { UserContext } from '../Context/UserContext'; 
import './Logout.css'
import { API_BASE_URL } from '../../../config/api';

const Logout = () => {
  const navigate = useNavigate();
  const { setUser } = useContext(UserContext); // Access the context to manage user state

  const handleLogout = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/logout/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${localStorage.getItem('authToken')}`, // Pass the token in the Authorization header
        },
      });

      if (response.ok) {
        // Clear user context or any stored user data
        setUser(null);
        localStorage.removeItem('authToken'); // Remove token from storage

        // Navigate to the login page or home page
        navigate('/');
      } else if (response.status === 401) {
        console.error('Unauthorized: Token is missing or invalid');
        // Optionally handle unauthorized cases, like forcing a logout
        navigate('/login');
      } else {
        console.error('Logout failed:', response.statusText);
      }
    } catch (error) {
      console.error('Error during logout:', error);
    }
  };

  return (
    <button onClick={handleLogout} className="logout-button">
      Logout
    </button>
  );
};

export default Logout;
