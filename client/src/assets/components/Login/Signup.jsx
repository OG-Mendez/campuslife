import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Signup.css';

const Signup = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [errors, setErrors] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [success, setSuccess] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate(); // Initialize useNavigate hook

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setErrors({ ...errors, [e.target.name]: '' }); // Clear error when user types
  };

  const isValidUsername = (username) => /^[a-zA-Z]{4,}[0-9]*$/.test(username);

  const isFormValid = () =>
    formData.username &&
    isValidUsername(formData.username) &&
    formData.email &&
    formData.password &&
    formData.password === formData.confirmPassword;

  const handleSubmit = async () => {
    if (isSubmitting) return;
    setIsSubmitting(true);
    setErrors({ username: '', email: '', password: '', confirmPassword: '' });
    setSuccess('');

    try {
      const response = await fetch(`${API_BASE_URL}/signup/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: formData.username,
          email: formData.email,
          password: formData.password,
          confirm_password: formData.confirmPassword,
        }),
      });

      const data = await response.json();
      if (response.ok) {
        setSuccess('Signup successful! Redirecting to login...');
        setFormData({ username: '', email: '', password: '', confirmPassword: '' });
        // Navigate to the login page after successful signup
        setTimeout(() => {
          navigate('/login');
        }, 2000); // Delay for 2 seconds before redirecting
      } else {
        // Set specific errors based on the response
        if (data.error === 'Username already taken') {
          setErrors((prev) => ({ ...prev, username: 'Username already taken' }));
        } else if (data.error === 'Email already taken') {
          setErrors((prev) => ({ ...prev, email: 'Email already taken' }));
        } else {
          setErrors((prev) => ({ ...prev, general: 'Signup failed. Please try again.' }));
        }
      }
    } catch (err) {
      setErrors((prev) => ({ ...prev, general: 'An error occurred. Please try again.' }));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="container4">
      <div className="form-container4 sign-up">
        <form onSubmit={(e) => { e.preventDefault(); handleSubmit(); }}>
          <h1>Welcome to Campuslife</h1>
          <p>Create a new account</p>
          
          <input
            type="text"
            placeholder="Username"
            name="username"
            value={formData.username}
            onChange={handleChange}
          />
          {errors.username && <p className="error">{errors.username}</p>}

          <input
            type="email"
            placeholder="Email"
            name="email"
            value={formData.email}
            onChange={handleChange}
          />
          {errors.email && <p className="error">{errors.email}</p>}

          <input
            type="password"
            placeholder="Password"
            name="password"
            value={formData.password}
            onChange={handleChange}
          />
          {errors.password && <p className="error">{errors.password}</p>}

          <input
            type="password"
            placeholder="Confirm Password"
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handleChange}
          />
          {errors.confirmPassword && <p className="error">{errors.confirmPassword}</p>}

          {errors.general && <p className="error">{errors.general}</p>}
          {success && <p className="success">{success}</p>}

          <button className="button4" type="submit" disabled={!isFormValid()}>
            {isSubmitting ? 'Please Wait...' : 'Sign Up'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Signup;
