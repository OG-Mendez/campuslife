import { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { UserContext } from '../Context/UserContext';
import { Link } from 'react-router-dom';
import './Login.css';

const Login = () => {
  const { setUser } = useContext(UserContext);
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    if (isSubmitting) return;
    setIsSubmitting(true);
    setError('');
    setSuccess('');
  
    try {
      const response = await fetch('https://campuslife-c9je.onrender.com/api/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: formData.username, password: formData.password }),
      });
  
      if (!response.ok) {
        const data = await response.json();
        if (data.detail === 'Invalid username or password') {
          setError('Username or password is incorrect.');
        } else {
          setError(data.detail || 'Invalid username or password. Please try again.');
        }
        return;
      }
  
      // If login is successful
      const data = await response.json();
      setSuccess('Login successful!');
      localStorage.setItem('token', data.token);
      setUser({ username: formData.username });
      navigate('/');
    } catch (err) {
      setError('Poor connection, try again.');
    } finally {
      setIsSubmitting(false);
    }
  };
  

  return (
    <div className="container4">
      <div className="form-container4 sign-in">
        <form onSubmit={(e) => { e.preventDefault(); handleSubmit(); }}>
          <h1>Welcome Back!</h1>
          <p>Login in to your account</p>
          <input
            type="text"
            placeholder="Username"
            name="username"
            value={formData.username}
            onChange={handleChange}
          />
          <input
            type="password"
            placeholder="Password"
            name="password"
            value={formData.password}
            onChange={handleChange}
          />
          
          <div className="links-container">
            <Link to="/forgot-password" className="left-link">Forgot Your Password?</Link>
            <Link to="/signup" className="right-link">Sign Up</Link>
          </div>
          
          {error && <p className="error">{error}</p>}
          {success && <p className="success">{success}</p>}
          <button className="button4" type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Logging in...' : 'Login'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;
