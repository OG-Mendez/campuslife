import React, { useState, useEffect } from 'react';
import { FaStar } from 'react-icons/fa';
import './AverageRating.css'

const AverageRating = ({ lodgeId }) => {
  const [rating, setRating] = useState(null);

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

  useEffect(() => {
    const fetchRating = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/average_rating/?id=${lodgeId}`);
        const data = await response.json();
        setRating(data.average_rating);
      } catch (error) {
        console.error('Error fetching rating:', error);
      }
    };

    fetchRating();
  }, [lodgeId]);

  return (
    <div className="average-rating">
      <FaStar style={{ color: 'black', fontSize: '1.3rem' }} />
      {/* Display 0 if rating is null (still loading or no average rating) */}
      <span className='A-rating'>{rating !== null ? rating : 0}</span>
    </div>
  );
};

export default AverageRating;
