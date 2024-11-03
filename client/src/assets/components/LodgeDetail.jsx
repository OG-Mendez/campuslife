import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import './LodgeDetail.css';

const LodgeDetail = () => {
  const { id } = useParams(); 
  const [lodge, setLodge] = useState(null);

  useEffect(() => {
    const fetchLodge = async () => {
      try {
        const response = await fetch(`https://campuslife-c9je.onrender.com/api/pictures/${id}`);
        if (!response.ok) throw new Error('Network response was not ok');

        const data = await response.json();
        setLodge(data); 
      } catch (error) {
        console.error('Error fetching lodge details:', error);
      }
    };

    fetchLodge();
  }, [id]);

  if (!lodge) return <p>Loading...</p>;

  return (
    <div className="lodge-detail">
      <div className="lodge-image-carousel">
        <img src={`https://campuslife-c9je.onrender.com${lodge.image}`} alt={lodge.lodge_name} />
        <div className='lodge-detail-h4'> <h4>{lodge.lodge_name}</h4></div>
      </div>
      <div className="lodge-info">
        <div className="lodge-info-item">
          <p>vacancy:</p>
          <strong>{lodge.vacancy || 'Not specified'}</strong> 
        </div>
        <div className="lodge-info-item">
          <p>Location:</p>
          <strong>{lodge.lodge_location || 'Unknown'}</strong> 
        </div>
        <div className="lodge-info-item">
          <p>Price:</p>
          <strong>{lodge.lodge_price ? `$${lodge.lodge_price}` : 'Price Unavailable'}</strong> 
        </div>
        <div className="lodge-info-item-cn">
          <p>Caretaker's number:</p> 
         <strong>{lodge.caretaker_contact || 'Not available'}</strong>  
        </div>
      </div>
    </div>
  );
};

export default LodgeDetail;
