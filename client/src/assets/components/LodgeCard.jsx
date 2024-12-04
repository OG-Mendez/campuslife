import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { LazyLoadImage } from 'react-lazy-load-image-component';
import 'react-lazy-load-image-component/src/effects/blur.css';
import './LodgeCard.css';

const LodgeCard = ({ lodge }) => {
  const location = useLocation(); 
  const vacancyText = lodge.available_vacancy > 0 ? 'Vacancy' : 'No Vacancy';
  const vacancyStyle = {
    color: lodge.available_vacancy > 0 ? 'green' : 'red',
  };

  return (
    <Link
      to={`/lodge/${lodge.id}${location.search}`} 
      className="lodge-card"
    >
      <div className="lodge-vacancy-badge" style={vacancyStyle}>
        {vacancyText}
      </div>
      <LazyLoadImage
        className="lodge-image"
        src={lodge.image}
        alt={lodge.lodge_name}
        effect="blur"
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
