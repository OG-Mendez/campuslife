import React from 'react';
import { Link } from 'react-router-dom';
import './LodgeCard.css';

const LodgeCard = ({ lodge }) => {
  return (
    <Link to={`/lodge/${lodge.id}`} className="lodge-card">
      <img
        src={`https://campuslife-c9je.onrender.com${lodge.image}`}
        alt={lodge.lodge_name}
        className="lodge-image"
      />
      <div className="lodge-info-1">
        <h3 className="lodge-name">{lodge.lodge_name}</h3>
        <p className="lodge-location">{lodge.lodge_location || 'Unknown Location'}</p>
        <p className="lodge-price">
          {lodge.lodge_price ? `₦${lodge.lodge_price} per year` : 'Price Unavailable'}
        </p>
      </div>
    </Link>
  );
};

export default LodgeCard;
