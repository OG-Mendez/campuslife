import React from 'react';
import { Link } from 'react-router-dom';
import './LodgeCard.css';

const LodgeCard = ({ lodge }) => {
  const vacancyText = lodge.available_vacancy > 0 ? 'Vacancy' : 'No Vacancy';
  const vacancyStyle = {
    color: lodge.available_vacancy > 0 ? 'green' : 'red',
  };

  return (
    <Link to={`/lodge/${lodge.id}`} className="lodge-card">
      <div className="lodge-vacancy-badge" style={vacancyStyle}>
        {vacancyText}
      </div>
      <img
        src={`https://campuslife-c9je.onrender.com${lodge.image}`}
        alt={lodge.lodge_name}
        className="lodge-image"
      />
      <div className="lodge-info-1">
        <h3 className="lodge-name">{lodge.lodge_name}</h3>
        <h4 className="lodge-location">{lodge.lodge_location || 'Unknown Location'}</h4>
        <h4 className="lodge-price">
          {lodge.lodge_price ? `₦${lodge.lodge_price} per year` : 'Price Unavailable'}
        </h4>
      </div>
    </Link>
  );
};

export default LodgeCard;
