import React, { useState, useEffect } from 'react';
import { FaStar } from 'react-icons/fa';
import './AverageRating.css'

const AverageRating = ({ lodgeId }) => {
  const [rating, setRating] = useState(null);

  useEffect(() => {
    const fetchRating = async () => {
      try {
        const response = await fetch(`https://campuslife-c9je.onrender.com/api/average_rating/?id=${lodgeId}`);
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
